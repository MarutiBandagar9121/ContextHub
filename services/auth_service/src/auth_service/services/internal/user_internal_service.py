from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth_service.config.settings import settings
from auth_service.models.refresh_token_model import RefreshToken
from auth_service.models.user_model import User
from auth_service.schemas.internal.user_schema import InternalRegisterRequest, InternalRegisterResponse, UserDetails, UserIdsRequestSchema
from auth_service.utils.jwt import create_access_token, create_refresh_token
from auth_service.utils.security import hash_password, hash_token

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

def register_user_via_invitation(payload: InternalRegisterRequest, db: Session) -> InternalRegisterResponse:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    try:
        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            is_verified=True,  # invitation token proves email ownership — skip OTP
        )
        db.add(user)
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    access_token = create_access_token(user_id=user.id, email=user.email)
    refresh_token = create_refresh_token(user_id=user.id)
    db.add(RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days),
    ))
    db.commit()

    return InternalRegisterResponse(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )