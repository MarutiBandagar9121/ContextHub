from typing import List

from sqlalchemy.orm import Session


from organization_service.const.organization_role_enum import OrganizationRoleEnum
from organization_service.models.organization_membership import OrganizationMembership
from organization_service.models.organization_model import Organization
from organization_service.schemas.organization_schema import CreateOrganization, OrganizationListResponse


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
    org_details = db.query(OrganizationMembership).filter(OrganizationMembership.user_id == user_id).all()
    
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

def delete_org(current_user_id:int, org_id:int,db:Session):
    orgs_to_delete = db.query(Organization).filter(Organization.owner_id == current_user_id, Organization.id == org_id)
    



    