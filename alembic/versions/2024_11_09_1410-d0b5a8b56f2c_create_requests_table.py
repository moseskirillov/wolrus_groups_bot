from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd0b5a8b56f2c'
down_revision: Union[str, None] = '765075b7e6a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(), nullable=False),
    sa.Column('is_processed', sa.Boolean(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['homegroups_bot.groups.id'], name=op.f('fk_requests_group_id_groups')),
    sa.ForeignKeyConstraint(['user_id'], ['homegroups_bot.users.id'], name=op.f('fk_requests_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_requests')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('requests', schema='homegroups_bot')
