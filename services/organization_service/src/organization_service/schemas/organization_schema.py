from datetime import datetime
from typing import List

from pydantic import BaseModel

from organization_service.const.organization_role_enum import OrganizationInvitationRoleEnum


class CreateOrganization(BaseModel):
    name: str
    description: str | None = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class UserDetail(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    user_role: str

class OrganizationFullDetailsResponse(OrganizationResponse):
    users: List[UserDetail]

class OrganizationListResponse(BaseModel):
    org_id: int
    name: str
    role: str
    description: str | None = None
    owner_id: int

class OrganizationInvitationPayload(BaseModel):
    org_id: int
    invited_by_id: int
    invited_user_email: str
    invited_for_role: OrganizationInvitationRoleEnum

class OrganizationInvitationResponse(BaseModel):
    id: int
    org_id: int
    invited_user_email: str
    invited_for_role: str

    model_config={
        "from_attributes": True
    }

class InvitationStatusCheckResponse(BaseModel):
    invitation_id:int
    invitation_token:str
    user_exists:bool
    user_email:str
    org_id:int
    org_name:str
    user_role:str
    token_expires_at:datetime