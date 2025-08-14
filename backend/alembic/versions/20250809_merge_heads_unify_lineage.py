"""merge multiple heads into single lineage

Revision ID: b5f4c3f9d5ab
Revises: ea2b7df7a9f1, ad00a873400b, add_analytics_fields_001
Create Date: 2025-08-09
"""
from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = 'b5f4c3f9d5ab'
down_revision = ('ea2b7df7a9f1', 'ad00a873400b', 'add_analytics_fields_001')
branch_labels = None
depends_on = None

def upgrade():
    # Pure merge – no operations. Consolidates multiple heads.
    pass

def downgrade():
    # Downgrade would re-split heads; typically not implemented for merges.
    pass
