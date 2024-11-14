"""create user leae table

Revision ID: 4944b164709d
Revises:
Create Date: 2023-11-19 23:04:53.414219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4944b164709d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_lease",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ip_addr", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user_lease")
