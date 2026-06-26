from typing import List

from fastapi import APIRouter
from fastapi import Depends

from auth_service.schemas.internal.user_schema import UserDetails, UserIdsRequestSchema
from auth_service.services.internal.user_internal_service import get_all_users_details
from auth_service.dependencies.db import get_db

router = APIRouter()
# path = /internal/api/v1/user

@router.post("/batch", response_model=List[UserDetails])
def get_users_details(payload: UserIdsRequestSchema, db = Depends(get_db)):
    return get_all_users_details(payload, db)