from datetime import datetime,timezone

from sqlalchemy import Column, DateTime,Integer,String, Boolean
from sqlalchemy.orm import relationship

from organization_service.db.base import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    owner_id = Column(Integer, nullable=False, index=True)
    description = Column(String(512), nullable=True) 
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    deleted_at = Column(
        DateTime(timezone=True),
        nullable = True,
        default = None)
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc))
    
    invitations = relationship(
        "OrganizationInvitations",
        back_populates="organization"
    )

    members = relationship(
        "OrganizationMembership",
        back_populates="organization",
    )
