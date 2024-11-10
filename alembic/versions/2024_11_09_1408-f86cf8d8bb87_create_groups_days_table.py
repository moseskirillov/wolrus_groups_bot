from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f86cf8d8bb87'
down_revision: Union[str, None] = 'a39a314d71dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('groups_days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['day_id'], ['homegroups_bot.days.id'], name=op.f('fk_groups_days_day_id_days')),
    sa.ForeignKeyConstraint(['group_id'], ['homegroups_bot.groups.id'], name=op.f('fk_groups_days_group_id_groups')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_groups_days')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('groups_days', schema='homegroups_bot')
