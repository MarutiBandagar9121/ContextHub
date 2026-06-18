from datetime import datetime, timezone

from auth_service.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc))

