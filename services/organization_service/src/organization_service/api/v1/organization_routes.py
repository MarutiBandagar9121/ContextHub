from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from organization_service.dependencies.db import get_db
from organization_service.dependencies.user import get_current_user_id
from organization_service.schemas.organization_schema import CreateOrganization, OrganizationFullDetailsResponse, OrganizationListResponse, OrganizationResponse
from organization_service.services import organization_service as org_service

router = APIRouter()
#path: api/v1/organization


@router.post("", response_model=OrganizationResponse)
def create_organization(
    payload:CreateOrganization,
    current_user_id:int = Depends(get_current_user_id),
    db:Session = Depends(get_db),
):
    return org_service.create_organization(payload, owner_id=current_user_id, db=db)

@router.get("", response_model=List[OrganizationListResponse])
def get_user_orgs(
    current_user_id:int = Depends(get_current_user_id),
    db:Session  = Depends(get_db)
):
    return org_service.get_users_org_deatails(current_user_id,db)

@router.get("/{org_id}", response_model=OrganizationFullDetailsResponse)
def get_org_details(org_id:int, db:Session = Depends(get_db)):
    return org_service.get_org_details(org_id,db)


@router.delete("/{org_id}")
def delete_org(
    org_id:int,
    current_user_id:int = Depends(get_current_user_id),
    db:Session = Depends(get_db),
    ):
    return org_service.delete_org(org_id,current_user_id,db)