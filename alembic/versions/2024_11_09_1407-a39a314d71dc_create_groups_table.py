from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a39a314d71dc'
down_revision: Union[str, None] = 'e6faa151d90e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.TIME(), nullable=False),
    sa.Column('age', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('is_open', sa.Boolean(), nullable=False),
    sa.Column('is_overflow', sa.Boolean(), nullable=False),
    sa.Column('is_multi_day', sa.Boolean(), nullable=False),
    sa.Column('leader_id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['homegroups_bot.districts.id'], name=op.f('fk_groups_district_id_districts')),
    sa.ForeignKeyConstraint(['leader_id'], ['homegroups_bot.groups_leaders.id'], name=op.f('fk_groups_leader_id_groups_leaders')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_groups')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('groups', schema='homegroups_bot')
