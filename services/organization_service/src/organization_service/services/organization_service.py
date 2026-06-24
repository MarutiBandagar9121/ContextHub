from typing import List
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from organization_service.const.organization_role_enum import OrganizationRoleEnum
from organization_service.models.organization_membership import OrganizationMembership
from organization_service.models.organization_model import Organization
from organization_service.schemas.organization_schema import CreateOrganization, OrganizationFullDetailsResponse, OrganizationListResponse


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

def get_org_details(org_id:int, db:Session)->OrganizationFullDetailsResponse:
    org_detail = db.query(Organization).filter(
        Organization.id == org_id,
        Organization.deleted_at.is_(None)
        ).first()
    if not org_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orgization not found")
    user_ids = db.query(OrganizationMembership).filter(
        OrganizationMembership.user_id == org_detail.id
        ).with_entities(
            OrganizationMembership.user_id
        ).all()
    user_ids = [row[0] for row in user_ids]
    return org_detail

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
    



    