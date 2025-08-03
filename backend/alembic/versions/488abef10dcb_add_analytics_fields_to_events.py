"""add_analytics_fields_to_events

Revision ID: 488abef10dcb
Revises: 7fe73f0ad0ce
Create Date: 2025-08-02 22:36:08.941217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '488abef10dcb'
down_revision: Union[str, None] = '7fe73f0ad0ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add analytics fields to events table for productivity insights"""
    
    # Add analytics fields to events table
    op.add_column('events', sa.Column('meeting_outcome', sa.String(50), nullable=False, server_default='neutral'))
    op.add_column('events', sa.Column('effectiveness_rating', sa.Integer(), nullable=False, server_default='3'))
    op.add_column('events', sa.Column('energy_level', sa.Integer(), nullable=False, server_default='3'))
    op.add_column('events', sa.Column('created_via', sa.String(20), nullable=False, server_default='manual'))
    op.add_column('events', sa.Column('actual_duration', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('planned_duration', sa.Integer(), nullable=True))
    
    # Add analytics indexes for optimized queries
    op.create_index(
        'idx_events_analytics', 
        'events', 
        ['user_id', 'start_time', 'meeting_outcome', 'effectiveness_rating']
    )
    
    # Add additional indexes for analytics performance
    op.create_index('idx_events_user_time', 'events', ['user_id', 'start_time'])
    op.create_index('idx_events_effectiveness', 'events', ['user_id', 'effectiveness_rating'])
    op.create_index('idx_events_outcome', 'events', ['user_id', 'meeting_outcome'])


def downgrade() -> None:
    """Remove analytics fields from events table"""
    
    # Drop indexes
    op.drop_index('idx_events_analytics', table_name='events')
    op.drop_index('idx_events_user_time', table_name='events')
    op.drop_index('idx_events_effectiveness', table_name='events')
    op.drop_index('idx_events_outcome', table_name='events')
    
    # Drop columns
    op.drop_column('events', 'meeting_outcome')
    op.drop_column('events', 'effectiveness_rating')
    op.drop_column('events', 'energy_level')
    op.drop_column('events', 'created_via')
    op.drop_column('events', 'actual_duration')
    op.drop_column('events', 'planned_duration')
