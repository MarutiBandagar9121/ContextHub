from typing import List

from fastapi import APIRouter, Query
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from auth_service.schemas.internal.user_schema import UserDetails, UserIdsRequestSchema
from auth_service.services.internal import user_internal_service as interna_user_service
from auth_service.dependencies.db import get_db

router = APIRouter()
# path = /internal/api/v1/user

@router.post("/batch", response_model=List[UserDetails])
def get_users_details(payload: UserIdsRequestSchema, db = Depends(get_db)):
    return interna_user_service.get_all_users_details(payload, db)

@router.get("", response_model=UserDetails)
def get_user_by_email(
    email:EmailStr = Query(..., description="Email address of the user to fetch"),
    db:Session = Depends(get_db)
):
    return interna_user_service.get_user_details_by_email(email,db)
