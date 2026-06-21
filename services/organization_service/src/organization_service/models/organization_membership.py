from organization_service.db.base import Base
from organization_service.const.organization_role_enum import OrganizationRoleEnum

from datetime import datetime,timezone

from sqlalchemy import Column, DateTime,Integer,String,ForeignKey, Enum
from sqlalchemy.orm import relationship

class OrganizationMembership(Base):
    __tablename__ = "organization_memberships"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    role = Column(Enum(OrganizationRoleEnum), nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    organization = relationship(
        "Organization",
        back_populates="members",
        lazy="joined",
        innerjoin=True,
    )