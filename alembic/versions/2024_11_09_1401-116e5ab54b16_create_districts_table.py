from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '116e5ab54b16'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('districts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_districts')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('districts', schema='homegroups_bot')
