"""add composite index on events(user_id, start_time)

Revision ID: ea2b7df7a9f1
Revises: 488abef10dcb
Create Date: 2025-08-09
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ea2b7df7a9f1'
down_revision = '488abef10dcb'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_index('ix_events_user_id_start_time', 'events', ['user_id', 'start_time'])

def downgrade() -> None:
    op.drop_index('ix_events_user_id_start_time', table_name='events')
