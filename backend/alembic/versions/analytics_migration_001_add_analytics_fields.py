"""add_analytics_fields_to_events

Revision ID: add_analytics_fields_001
Revises: 7fe73f0ad0ce
Create Date: 2025-08-02 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_analytics_fields_001'
down_revision = '7fe73f0ad0ce'
branch_labels = None
depends_on = None


def upgrade():
    """No-op (duplicate of later analytics migration 488abef10dcb)."""
    pass


def downgrade():
    # Nothing to undo since upgrade was a no-op
    pass
