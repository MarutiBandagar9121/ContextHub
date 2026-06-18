from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Enum, String

from auth_service.db.base import Base
from auth_service.const.otp_types_enum import OtpTypesEnum


class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(OtpTypesEnum), nullable=False)
    otp = Column(String(8), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc))
