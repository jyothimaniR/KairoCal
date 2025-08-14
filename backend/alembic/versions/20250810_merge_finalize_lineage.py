"""Merge to finalize single-head lineage after index and timestamp migrations

Revision ID: merge_finalize_20250810
Revises: b5f4c3f9d5ab, ts_defaults_users_20250810
Create Date: 2025-08-10
"""

from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = 'merge_finalize_20250810'

down_revision = ('b5f4c3f9d5ab', 'ts_defaults_users_20250810')
branch_labels = None
depends_on = None


def upgrade():
    # Pure merge – no schema changes. Unifies branches into a single head.
    pass


def downgrade():
    # Downgrade would re-split branches; typically omitted for merge revisions.
    pass
