
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth_service.schemas.user_schema import UserOtpVerificationRequestSchema, UserRegisterRequestSchema, UserRegisterResponseSchema, UserOtpVerificationResponseSchema  
from auth_service.models.user_model import User
from auth_service.models.otp_model import Otp
from auth_service.models.refresh_token_model import RefreshToken
from auth_service.utils.security import hash_password, hash_token
from auth_service.const.otp_types_enum import OtpTypesEnum
from auth_service.utils.otp import generate_otp
from auth_service.utils.jwt import create_access_token, create_refresh_token
from auth_service.config.settings import settings


def register_new_user(payload: UserRegisterRequestSchema, db: Session) -> UserRegisterResponseSchema:
    """Registers a new user in the system."""
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        if not user.is_verified:
            user.first_name = payload.first_name
            user.last_name = payload.last_name
            user.hashed_password = hash_password(payload.password)

            otp = Otp(
                type=OtpTypesEnum.EMAIL_VERIFICATION,
                otp=generate_otp(),
                user_id=user.id,
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
            )
            db.add(otp)
            db.commit()
            return user
        else:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=hash_password(payload.password)
        )
        db.add(user)
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = Otp(
        type=OtpTypesEnum.EMAIL_VERIFICATION,
        otp=generate_otp(),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )

    db.add(otp)
    db.commit()
    return user

def verify_otp(payload: UserOtpVerificationRequestSchema, db: Session):
    """Verifies the OTP for a user."""
    otp_record = db.query(Otp).filter(Otp.user_id == payload.id, Otp.otp == payload.otp).first()
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if otp_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    if otp_record.type != OtpTypesEnum.EMAIL_VERIFICATION:
        raise HTTPException(status_code=400, detail="Invalid OTP type")
    
    if otp_record.is_used:
        raise HTTPException(status_code=400, detail="OTP has already been used")
    
    user = db.query(User).filter(User.id == payload.id).first()
    if user:
        user.is_verified = True
        otp_record.is_used = True

        access_token = create_access_token(user_id=user.id, email=user.email)
        refresh_token = create_refresh_token(user_id=user.id)

        refresh_token_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        )
        db.add(refresh_token_record)
        db.commit()

        return UserOtpVerificationResponseSchema(
            message="OTP verified successfully",
            access_token=access_token,
            refresh_token=refresh_token
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")