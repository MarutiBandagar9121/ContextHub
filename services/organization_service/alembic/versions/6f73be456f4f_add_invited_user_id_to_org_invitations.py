"""add invited_user_id to org invitations

Revision ID: 6f73be456f4f
Revises: c11bf5746499
Create Date: 2026-06-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f73be456f4f'
down_revision: Union[str, Sequence[str], None] = 'c11bf5746499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('organization_invitations', sa.Column('invited_user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_organization_invitations_invited_user_id'), 'organization_invitations', ['invited_user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_organization_invitations_invited_user_id'), table_name='organization_invitations')
    op.drop_column('organization_invitations', 'invited_user_id')
