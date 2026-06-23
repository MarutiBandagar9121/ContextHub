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

class OrganizationListResponse(BaseModel):
    org_id: int
    name: str
    role: str
    description: str | None = None
    owner_id: int