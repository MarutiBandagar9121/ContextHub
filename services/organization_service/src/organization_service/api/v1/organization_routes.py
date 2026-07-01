from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from organization_service.dependencies.db import get_db
from organization_service.dependencies.user import get_current_user_id
from organization_service.schemas.organization_schema import AcceptInvitationRegisterRequest, AcceptInvitationRegisterResponse, CreateOrganization, InvitationStatusCheckResponse, OrganizationFullDetailsResponse, OrganizationInvitationPayload, OrganizationInvitationResponse, OrganizationListResponse, OrganizationResponse
from organization_service.services import organization_service as org_service
from organization_service.dependencies import db

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
async def get_org_details(
    org_id:int, 
    current_user_id:int = Depends(get_current_user_id),
    db:Session = Depends(get_db),
    ):
    return await org_service.get_org_details(org_id,db)


@router.delete("/{org_id}")
def delete_org(
    org_id:int,
    current_user_id:int = Depends(get_current_user_id),
    db:Session = Depends(get_db),
    ):
    return org_service.delete_org(org_id,current_user_id,db)

@router.post("/invitation", response_model=OrganizationInvitationResponse, status_code=status.HTTP_201_CREATED)
def create_org_invitation(
    payload: OrganizationInvitationPayload, 
    current_user_id:int = Depends(get_current_user_id),
    db: Session = Depends(get_db)):
    return org_service.make_org_invitation(payload,current_user_id, db)

@router.get("/invitation/{invitation_token}", response_model=InvitationStatusCheckResponse, status_code=status.HTTP_200_OK)
async def check_invitation_status(invitation_token:str, db:Session = Depends(get_db)):
    return await org_service.check_invitation_status(invitation_token, db)

@router.post("/invitation/{invitation_token}/accept", response_model=AcceptInvitationRegisterResponse, status_code=status.HTTP_200_OK)
async def accept_invitation(
    invitation_token:str,
    payload:AcceptInvitationRegisterRequest,
    response: Response,
    db:Session = Depends(get_db)):
    return await org_service.accept_invitation_register(invitation_token, payload, response, db)