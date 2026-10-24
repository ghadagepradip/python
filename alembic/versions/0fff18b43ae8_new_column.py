"""new column

Revision ID: 0fff18b43ae8
Revises: 511c711da97f
Create Date: 2026-10-24 19:18:30.122600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fff18b43ae8'
down_revision: Union[str, Sequence[str], None] = '511c711da97f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
