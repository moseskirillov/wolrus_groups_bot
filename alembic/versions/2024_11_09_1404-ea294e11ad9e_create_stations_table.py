from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ea294e11ad9e'
down_revision: Union[str, None] = '903f59b13fb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('stations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('callback_data', sa.String(length=255), nullable=False),
    sa.Column('transport_id', sa.Integer(), nullable=False),
    sa.Column('line_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['line_id'], ['homegroups_bot.lines.id'], name=op.f('fk_stations_line_id_lines')),
    sa.ForeignKeyConstraint(['transport_id'], ['homegroups_bot.transports.id'], name=op.f('fk_stations_transport_id_transports')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_stations')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('stations', schema='homegroups_bot')
