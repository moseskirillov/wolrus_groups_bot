from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7f01e1c3b7a9'
down_revision: Union[str, None] = '3680920209ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('regional_leaders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['homegroups_bot.users.id'], name=op.f('fk_regional_leaders_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_regional_leaders')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('regional_leaders', schema='homegroups_bot')
