
from datetime import datetime

from pydantic import BaseModel

class UserRegisterRequestSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str
    password: str

class UserRegisterResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserOtpVerificationRequestSchema(BaseModel):
    id: int
    otp: str

class UserOtpResendRequestSchema(BaseModel):
    id: int

class UserOtpVerificationResponseSchema(BaseModel):
    message: str
    access_token: str

class UserOtpResendResponseSchema(BaseModel):
    message: str

class UserLoginRequestSchema(BaseModel):
    email: str
    password: str

class UserLoginResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    email: str
    access_token: str

class UserLogoutResponseSchema(BaseModel):
    message: str

class TokenRefreshResponseSchema(BaseModel):
    access_token: str