from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '016cffe94be2'
down_revision: Union[str, None] = 'd0b5a8b56f2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('districts', sa.Column('is_mo', sa.Boolean(), nullable=True), schema='homegroups_bot')


def downgrade() -> None:
    op.drop_column('districts', 'is_mo', schema='homegroups_bot')
