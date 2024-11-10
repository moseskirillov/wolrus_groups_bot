from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e6faa151d90e'
down_revision: Union[str, None] = '7f01e1c3b7a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('groups_leaders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('regional_leader_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['regional_leader_id'], ['homegroups_bot.regional_leaders.id'], name=op.f('fk_groups_leaders_regional_leader_id_regional_leaders')),
    sa.ForeignKeyConstraint(['user_id'], ['homegroups_bot.users.id'], name=op.f('fk_groups_leaders_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_groups_leaders')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('groups_leaders', schema='homegroups_bot')
