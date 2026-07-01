from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pydantic import EmailStr

from auth_service.schemas.internal.user_schema import UserIdsRequestSchema
from auth_service.models.user_model import User
from auth_service.schemas.internal.user_schema import UserDetails

def get_all_users_details(payload : UserIdsRequestSchema, db:Session)->List[UserDetails]:
    print("get user batch request schema: ",payload)
    users = db.query(User).filter(
        User.id.in_(payload.user_ids)
    ).all()

    if not users:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND, 
           detail="Users not found"
        )
    return users

def get_user_details_by_email(
        email: EmailStr,
        db: Session
)->UserDetails:
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user