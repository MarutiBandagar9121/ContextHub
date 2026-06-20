from organization_service.db.base import Base
from datetime import datetime,timezone
from sqlalchemy import Column, DateTime,Integer,String

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    owner_id = Column(Integer, nullable=False)
    description = Column(String(512), nullable=True)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc))
