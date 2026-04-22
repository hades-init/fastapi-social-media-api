"""Add additional columns to posts table

Revision ID: 4860e62067b4
Revises: a59d9b527a75
Create Date: 2026-04-22 16:33:09.340772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4860e62067b4'
down_revision: Union[str, Sequence[str], None] = 'a59d9b527a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        table_name="posts",
        column=sa.Column("published", sa.Boolean, nullable=False, server_default='True')
    )
    op.add_column(
        table_name="posts",
        column=sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                         server_default=sa.func.now(), nullable=False)
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        table_name="posts",
        column_name="published",
    )
    op.drop_column(
        table_name="posts",
        column_name="created_at",
    )
