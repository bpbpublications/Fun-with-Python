"""add whitelist

Revision ID: 089224738104
Revises: 83982abde4ad
Create Date: 2023-12-20 20:07:25.260347

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "089224738104"
down_revision: Union[str, None] = "83982abde4ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "white_list_lease",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("mac_address", sa.String(50), unique=True),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column("updated_at", sa.DateTime, default=datetime.now),
    )


def downgrade() -> None:
    op.drop_table("white_list_lease")
