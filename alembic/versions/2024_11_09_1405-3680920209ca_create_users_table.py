from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3680920209ca'
down_revision: Union[str, None] = 'ea294e11ad9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('telegram_login', sa.String(length=255), nullable=True),
    sa.Column('telegram_id', sa.String(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('last_login', sa.TIMESTAMP(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('telegram_id', name=op.f('uq_users_telegram_id')),
    sa.UniqueConstraint('telegram_login', name=op.f('uq_users_telegram_login')),
    schema='homegroups_bot')


def downgrade() -> None:
    op.drop_table('users', schema='homegroups_bot')
