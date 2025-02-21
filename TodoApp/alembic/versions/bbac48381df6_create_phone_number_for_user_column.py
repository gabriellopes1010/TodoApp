"""create phone number for user column

Revision ID: bbac48381df6
Revises: 
Create Date: 2025-02-18 16:31:41.375997

"""

import routers
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bbac48381df6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
