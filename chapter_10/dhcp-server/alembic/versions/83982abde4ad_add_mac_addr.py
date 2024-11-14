"""add mac addr

Revision ID: 83982abde4ad
Revises: b0b4ac080f74
Create Date: 2023-11-20 22:34:09.888628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83982abde4ad"
down_revision: Union[str, None] = "b0b4ac080f74"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_lease", sa.Column("mac_address", sa.String(50)))


def downgrade() -> None:
    pass
