from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth_service.schemas.user_schema import UserRegisterRequestSchema, UserRegisterResponseSchema, UserOtpVerificationRequestSchema, UserOtpVerificationResponseSchema
from auth_service.dependencies.db import get_db
from auth_service.services import user_serivice

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponseSchema)
def register_user(request: UserRegisterRequestSchema,  db: Session = Depends(get_db)):
    """Endpoint to register a new user."""
    return user_serivice.register_new_user(payload=request, db=db)

@router.post("/verify_otp", response_model=UserOtpVerificationResponseSchema)
def verify_otp(payload: UserOtpVerificationRequestSchema, db: Session = Depends(get_db)):
    """Endpoint to verify OTP."""
    return user_serivice.verify_otp(payload=payload, db=db)