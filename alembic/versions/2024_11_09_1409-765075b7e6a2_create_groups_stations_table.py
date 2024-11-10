from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '765075b7e6a2'
down_revision: Union[str, None] = 'f86cf8d8bb87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('groups_stations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('station_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['homegroups_bot.groups.id'], name=op.f('fk_groups_stations_group_id_groups')),
    sa.ForeignKeyConstraint(['station_id'], ['homegroups_bot.stations.id'], name=op.f('fk_groups_stations_station_id_stations')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_groups_stations')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('groups_stations', schema='homegroups_bot')
