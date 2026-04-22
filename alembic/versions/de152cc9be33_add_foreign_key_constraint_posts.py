"""Add foreign key constraint to posts table

Revision ID: de152cc9be33
Revises: 60409bdec05a
Create Date: 2026-04-22 16:54:37.423622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de152cc9be33'
down_revision: Union[str, Sequence[str], None] = '60409bdec05a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        table_name="posts", 
        column=sa.Column("owner_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        "posts_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        constraint_name="posts_users_fkey", 
        table_name="posts"
    )
    op.drop_column(
        table_name="posts", 
        column_name="owner_id"
    )
