from auth_service.db.base import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc))

