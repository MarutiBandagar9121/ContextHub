
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth_service.schemas.user_schema import TokenRefreshResponseSchema, UserLoginRequestSchema, UserLoginResponseSchema, UserLogoutResponseSchema, UserOtpResendRequestSchema, UserOtpResendResponseSchema, UserOtpVerificationRequestSchema, UserRegisterRequestSchema, UserRegisterResponseSchema, UserOtpVerificationResponseSchema
from auth_service.models.user_model import User
from auth_service.models.otp_model import Otp
from auth_service.models.refresh_token_model import RefreshToken
from auth_service.utils.security import hash_password, hash_token, verify_hashed_password
from auth_service.const.otp_types_enum import OtpTypesEnum
from auth_service.utils.otp import generate_otp
from auth_service.utils.jwt import create_access_token, create_refresh_token, decode_token
from auth_service.utils.cookies import REFRESH_TOKEN_COOKIE_NAME, clear_refresh_token_cookie, set_refresh_token_cookie
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

def _revoke_active_refresh_tokens(user_id: int, db: Session) -> None:
    """Revokes all of a user's refresh tokens that haven't been revoked yet."""
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None)
    ).update({"revoked_at": datetime.now(timezone.utc)})

def _issue_refresh_token(user_id: int, db: Session) -> str:
    """Revokes the user's existing refresh tokens and persists a new one, so
    only one refresh token is ever active per user."""
    refresh_token = create_refresh_token(user_id=user_id)
    _revoke_active_refresh_tokens(user_id, db)
    db.add(RefreshToken(
        user_id=user_id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    ))
    return refresh_token

def verify_otp(payload: UserOtpVerificationRequestSchema, db: Session, response: Response) -> UserOtpVerificationResponseSchema:
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
        refresh_token = _issue_refresh_token(user.id, db)
        db.commit()

        set_refresh_token_cookie(response, refresh_token)

        return UserOtpVerificationResponseSchema(
            message="OTP verified successfully",
            access_token=access_token
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")

def resend_otp(payload: UserOtpResendRequestSchema, db: Session) -> UserOtpResendResponseSchema:
    """Resends the OTP for a user."""
    user = db.query(User).filter(User.id == payload.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified")

    otp_record = db.query(Otp).filter(Otp.user_id == payload.id, Otp.type == OtpTypesEnum.EMAIL_VERIFICATION).first()
    if otp_record:
        if otp_record.is_used:
            raise HTTPException(status_code=400, detail="OTP has already been used")

        otp_record.expires_at = datetime.now(timezone.utc)
        db.commit()

    otp = Otp(
        type=OtpTypesEnum.EMAIL_VERIFICATION,
        otp=generate_otp(),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )
    db.add(otp)
    db.commit()

    return UserOtpResendResponseSchema(message="OTP resent successfully")

def login_user(payload: UserLoginRequestSchema, db: Session, response: Response) -> UserLoginResponseSchema:
    """Logs in a user."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User is not verified")


    if not verify_hashed_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(user_id=user.id, email=user.email)
    refresh_token = _issue_refresh_token(user.id, db)
    db.commit()

    set_refresh_token_cookie(response, refresh_token)

    return UserLoginResponseSchema(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        access_token=access_token
    )

def logout_user(db: Session, request: Request, response: Response) -> UserLogoutResponseSchema:
    """Logs out a user by revoking the refresh token cookie they presented, if any."""
    refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
    if refresh_token:
        try:
            decoded = decode_token(refresh_token)
        except jwt.PyJWTError:
            decoded = None

        if decoded and decoded.get("type") == "refresh":
            token_record = db.query(RefreshToken).filter(
                RefreshToken.token_hash == hash_token(refresh_token)
            ).first()

            if token_record and token_record.revoked_at is None:
                token_record.revoked_at = datetime.now(timezone.utc)
                db.commit()

    clear_refresh_token_cookie(response)

    return UserLogoutResponseSchema(message="Logged out successfully")

def refresh_access_token(db: Session, request: Request, response: Response) -> TokenRefreshResponseSchema:
    """Issues a new access token (and rotates the refresh token) from the refresh token cookie."""
    refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        decoded = decode_token(refresh_token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_record = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hash_token(refresh_token)
    ).first()

    if not token_record or token_record.revoked_at is not None:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    if token_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token has expired")

    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(user_id=user.id, email=user.email)
    new_refresh_token = _issue_refresh_token(user.id, db)
    db.commit()

    set_refresh_token_cookie(response, new_refresh_token)

    return TokenRefreshResponseSchema(access_token=access_token)
