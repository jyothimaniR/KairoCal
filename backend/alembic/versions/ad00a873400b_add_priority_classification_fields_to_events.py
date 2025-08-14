"""Add priority classification fields to events table

Revision ID: ad00a873400b
Revises: 7fe73f0ad0ce
Create Date: 2025-07-30 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ad00a873400b'
down_revision: Union[str, None] = '7fe73f0ad0ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: superseded by consolidated later migration path.
    pass


def downgrade() -> None:
    # Nothing to roll back (no-op upgrade)
    pass
