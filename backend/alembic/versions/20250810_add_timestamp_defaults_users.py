"""Add defaults for users.created_at / updated_at and backfill

Revision ID: ts_defaults_users_20250810
Revises: ea2b7df7a9f1
Create Date: 2025-08-10
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'ts_defaults_users_20250810'
down_revision = 'ea2b7df7a9f1'
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    # Set DEFAULT now() for created_at / updated_at if not already
    try:
        conn.execute(text("ALTER TABLE users ALTER COLUMN created_at SET DEFAULT (TIMEZONE('UTC', now()))"))
    except Exception:
        pass
    try:
        conn.execute(text("ALTER TABLE users ALTER COLUMN updated_at SET DEFAULT (TIMEZONE('UTC', now()))"))
    except Exception:
        pass
    # Backfill NULLs
    conn.execute(text("UPDATE users SET created_at = TIMEZONE('UTC', now()) WHERE created_at IS NULL"))
    conn.execute(text("UPDATE users SET updated_at = TIMEZONE('UTC', now()) WHERE updated_at IS NULL"))


def downgrade() -> None:
    conn = op.get_bind()
    # Remove defaults (keep data)
    try:
        conn.execute(text("ALTER TABLE users ALTER COLUMN created_at DROP DEFAULT"))
    except Exception:
        pass
    try:
        conn.execute(text("ALTER TABLE users ALTER COLUMN updated_at DROP DEFAULT"))
    except Exception:
        pass
