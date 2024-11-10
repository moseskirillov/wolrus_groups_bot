from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '903f59b13fb3'
down_revision: Union[str, None] = '1b0f9cd6c178'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_days')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('days', schema='homegroups_bot')
