from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '5e24c28e0800'
down_revision: Union[str, None] = '016cffe94be2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('districts', sa.Column('callback_data', sa.String(length=255), nullable=True),
                  schema='homegroups_bot')
    op.alter_column('districts', 'is_mo',
                    existing_type=sa.BOOLEAN(),
                    nullable=False,
                    schema='homegroups_bot')


def downgrade() -> None:
    op.alter_column('districts', 'is_mo',
                    existing_type=sa.BOOLEAN(),
                    nullable=True,
                    schema='homegroups_bot')
    op.drop_column('districts', 'callback_data', schema='homegroups_bot')
