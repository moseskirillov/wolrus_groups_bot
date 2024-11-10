from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '968766ffa963'
down_revision: Union[str, None] = '116e5ab54b16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('lines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('color', sa.String(length=255), nullable=True),
    sa.Column('callback_data', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_lines')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('lines', schema='homegroups_bot')
