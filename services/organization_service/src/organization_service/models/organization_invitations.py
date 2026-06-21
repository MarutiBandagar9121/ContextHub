from datetime import datetime,timezone

from sqlalchemy import Column, Index, Integer, String, Boolean, Enum, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship

from organization_service.db.base import Base
from organization_service.const.organization_role_enum import OrganizationRoleEnum
from organization_service.const.organization_invitation_status_enum import OrganizationInvitationStatusEnum

class OrganizationInvitations(Base):
    __tablename__ = "organization_invitations"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    invitation_token = Column(String, unique=True,nullable=False, index=True)
    invited_by_id = Column(Integer, nullable=False, index=True)
    invited_user_email = Column(String, nullable=False, index=True)
    invitation_status = Column(
        Enum(OrganizationInvitationStatusEnum),
        nullable=False,
        default=OrganizationInvitationStatusEnum.PENDING,
    )
    invited_for_role = Column(Enum(OrganizationRoleEnum), nullable=False)
    is_new_user = Column(Boolean,default=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default= lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index(
            "uq_pending_invite_per_org_email",
            "org_id",
            "invited_user_email",
            unique=True,
            postgresql_where=text("invitation_status = 'pending'"),
        ),
    )

    organization = relationship(
        "Organization",
        back_populates="invitations",
        lazy="joined",
        innerjoin=True,
    )
