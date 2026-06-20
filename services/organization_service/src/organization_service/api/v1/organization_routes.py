from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from organization_service.dependencies.db import get_db
from organization_service.dependencies.user import get_current_user_id
from organization_service.schemas.organization_schema import CreateOrganization, OrganizationListResponse, OrganizationResponse
from organization_service.services import organization_service as org_service

router = APIRouter()


@router.post("", response_model=OrganizationResponse)
def create_organization(
    payload:CreateOrganization,
    current_user_id:int = Depends(get_current_user_id),
    db:Session = Depends(get_db),
):
    return org_service.create_organization(payload, owner_id=current_user_id, db=db)

@router.get("", response_model=OrganizationListResponse)
def get_user_orgs(
    current_user_id:int = Depends(get_current_user_id),
    db:Session  = Depends(get_db)
):
    return org_service.get_all_user_org_deatails(current_user_id,db)