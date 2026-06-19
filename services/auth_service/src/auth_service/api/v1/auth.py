from fastapi import APIRouter, Request, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth_service.schemas.user_schema import TokenRefreshResponseSchema, UserLoginRequestSchema, UserLoginResponseSchema, UserLogoutResponseSchema, UserOtpResendRequestSchema, UserOtpResendResponseSchema, UserRegisterRequestSchema, UserRegisterResponseSchema, UserOtpVerificationRequestSchema, UserOtpVerificationResponseSchema
from auth_service.dependencies.db import get_db
from auth_service.services import user_serivice

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponseSchema)
def register_user(request: UserRegisterRequestSchema,  db: Session = Depends(get_db)):
    """Endpoint to register a new user."""
    return user_serivice.register_new_user(payload=request, db=db)

@router.post("/verify_otp", response_model=UserOtpVerificationResponseSchema)
def verify_otp(payload: UserOtpVerificationRequestSchema, response: Response, db: Session = Depends(get_db)):
    """Endpoint to verify OTP."""
    return user_serivice.verify_otp(payload=payload, db=db, response=response)

@router.post("/resend_otp", response_model=UserOtpResendResponseSchema)
def resend_otp(payload: UserOtpResendRequestSchema, db: Session = Depends(get_db)):
    """Endpoint to resend OTP."""
    return user_serivice.resend_otp(payload=payload, db=db)

@router.post("/login", response_model=UserLoginResponseSchema)
def login_user(payload: UserLoginRequestSchema, response: Response, db: Session = Depends(get_db)):
    """Endpoint to log in a user."""
    return user_serivice.login_user(payload=payload, db=db, response=response)

@router.post("/logout", response_model=UserLogoutResponseSchema)
def logout_user(request: Request, response: Response, db: Session = Depends(get_db)):
    """Endpoint to log out a user."""
    return user_serivice.logout_user(db=db, request=request, response=response)

@router.post("/refresh", response_model=TokenRefreshResponseSchema)
def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
    """Endpoint to issue a new access token from the refresh token cookie."""
    return user_serivice.refresh_access_token(db=db, request=request, response=response)