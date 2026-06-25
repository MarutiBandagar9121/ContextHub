from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from auth_service.schemas.internal.user_schema import UserIdsRequestSchema
from auth_service.models.user_model import User
from auth_service.schemas.internal.user_schema import UserDetails

def get_all_users_details(payload : UserIdsRequestSchema, db:Session)->List[UserDetails]:
    users = db.query(User).filter(
        User.id.in_(payload.user_ids)
    ).all()

    if not users:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND, 
           detail="Users not found"
        )
    
    return users