"""add arp table

Revision ID: 3447f92780da
Revises: 089224738104
Create Date: 2023-12-28 21:35:39.851236

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3447f92780da"
down_revision: Union[str, None] = "089224738104"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "arp_record",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ip_addr", sa.String(50), nullable=False),
        sa.Column("mac_address", sa.String(50), unique=True),
        sa.Column("created_at", sa.DateTime, default=datetime.now),
        sa.Column("updated_at", sa.DateTime, default=datetime.now),
    )


def downgrade() -> None:
    op.drop_table("arp_record")
