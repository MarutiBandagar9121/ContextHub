from typing import List
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from organization_service.const.organization_role_enum import OrganizationRoleEnum
from organization_service.models.organization_membership import OrganizationMembership
from organization_service.models.organization_model import Organization
from organization_service.schemas.organization_schema import CreateOrganization, OrganizationFullDetailsResponse, OrganizationListResponse, UserDetail
from organization_service.http_clients.user_service_client import UserServiceClient
from organization_service.schemas.user_schema import UserServiceUserDetailsResponse


def create_organization(payload: CreateOrganization, owner_id: int, db: Session) -> Organization:
    """Creates an organization and its owner's membership row in one
    transaction, so listing/visibility logic only ever has to query
    organization_memberships."""
    organization = Organization(
        name=payload.name,
        description=payload.description,
        owner_id=owner_id,
    )
    db.add(organization)
    db.flush()

    membership = OrganizationMembership(
        organization_id=organization.id,
        user_id=owner_id,
        role=OrganizationRoleEnum.OWNER,
    )
    db.add(membership)
    db.commit()
    db.refresh(organization)

    return organization

def get_users_org_deatails(user_id:int, db:Session)->List[OrganizationListResponse]:
    org_details = db.query(OrganizationMembership).join(
        Organization, Organization.id == OrganizationMembership.organization_id).filter(
            OrganizationMembership.user_id == user_id,
            Organization.deleted_at.is_(None)
        ).all()
    
    response: List[OrganizationListResponse] = list()
    for org_detail in org_details:
        response.append(OrganizationListResponse(
            org_id = org_detail.organization_id,
            name = org_detail.organization.name,
            role = org_detail.role,
            description= org_detail.organization.description,
            owner_id = org_detail.organization.owner_id,
        ))
    return response

# organization_service.py
async def get_org_details(org_id: int, db: Session) -> OrganizationFullDetailsResponse:
    # 1. Get organization details
    org_detail = db.query(Organization).filter(
        Organization.id == org_id,
        Organization.deleted_at.is_(None)
    ).first()
    
    if not org_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    # 2. Get all memberships with roles
    memberships = db.query(OrganizationMembership).filter(
        OrganizationMembership.organization_id == org_detail.id
    ).all()
    
    # Extract user IDs and create a mapping of user_id -> role
    user_id_to_role = {membership.user_id: membership.role for membership in memberships}
    user_ids = list(user_id_to_role.keys())
    
    user_client = UserServiceClient()
    try:
        user_details:List[UserServiceUserDetailsResponse] = await user_client.get_users_by_ids(user_ids)
    except Exception as e:
        # logger.error(f"Failed to fetch user details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch user details: {str(e)}")
    
    # 4. Combine user details with roles
    users_response = []
    for user in user_details:
        # print(f"user in loop: {user}")
        users_response.append(
            UserDetail(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                user_role=user_id_to_role.get(user.user_id, "MEMBER")
            )
        )
    
    # 5. Return complete response
    return OrganizationFullDetailsResponse(
        id=org_detail.id,
        name=org_detail.name,
        description=org_detail.description,
        owner_id=org_detail.owner_id,
        created_at=org_detail.created_at,
        updated_at=org_detail.updated_at,
        users=users_response
    )
    
    # 5. Return complete response
    return OrganizationFullDetailsResponse(
        id=org_detail.id,
        name=org_detail.name,
        description=org_detail.description,
        owner_id=org_detail.owner_id,
        created_at=org_detail.created_at,
        updated_at=org_detail.updated_at,
        users=users_response
    )
def delete_org(org_id:int, current_user_id:int, db:Session):
    org_to_delete = db.query(Organization).filter(
        Organization.owner_id == current_user_id, 
        Organization.id == org_id,
        Organization.deleted_at.is_(None)
        ).first()
    if not org_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization does not exist")
    try:
        org_to_delete.deleted_at = datetime.now(timezone.utc)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="Organization deletion failed.")
    return {"message":"Organization deletion successfull"}
    



    