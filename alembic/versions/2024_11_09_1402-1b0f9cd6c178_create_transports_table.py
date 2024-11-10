from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '1b0f9cd6c178'
down_revision: Union[str, None] = '968766ffa963'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('transports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('callback_data', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_transports')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('transports', schema='homegroups_bot')
