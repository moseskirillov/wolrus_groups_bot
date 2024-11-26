from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "9161100c313e"
down_revision: Union[str, None] = "4bc38ff10bfa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_youth_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        schema="homegroups_bot",
    )


def downgrade() -> None:
    op.drop_column("users", "is_youth_admin", schema="homegroups_bot")
