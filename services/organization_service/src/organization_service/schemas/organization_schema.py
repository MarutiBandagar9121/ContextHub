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

class OrganizationMemberDetails(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str

class OrganizationListResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    members: List[OrganizationMemberDetails]
    created_at: datetime
    updated_at: datetime
