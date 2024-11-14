"""add datetime columns

Revision ID: b0b4ac080f74
Revises: 4944b164709d
Create Date: 2023-11-19 23:55:45.972206

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b0b4ac080f74"
down_revision: Union[str, None] = "4944b164709d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_lease", sa.Column("created_at", sa.DateTime, default=datetime.now))
    op.add_column("user_lease", sa.Column("updated_at", sa.DateTime, default=datetime.now))


def downgrade() -> None:
    pass
