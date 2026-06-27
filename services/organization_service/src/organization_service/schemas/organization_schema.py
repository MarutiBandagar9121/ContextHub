from datetime import datetime
from typing import List

from pydantic import BaseModel


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
    user_id: int
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
    invited_for_role: str
