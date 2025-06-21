"""Add new entities PomodoroRound and PomodoroSession

Revision ID: a50f4f5cd0cf
Revises: 2d6f4945a9ff
Create Date: 2025-05-25 13:10:15.354438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a50f4f5cd0cf'
down_revision: Union[str, None] = '2d6f4945a9ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
