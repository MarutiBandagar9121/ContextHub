from enum import Enum

class OrganizationInvitationStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REJECTED = "rejected"