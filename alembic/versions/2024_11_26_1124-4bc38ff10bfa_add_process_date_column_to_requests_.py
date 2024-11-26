from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "4bc38ff10bfa"
down_revision: Union[str, None] = "c2c1df11d726"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "requests",
        sa.Column("process_date", sa.TIMESTAMP(), nullable=True),
        schema="homegroups_bot",
    )


def downgrade() -> None:
    op.drop_column("requests", "process_date", schema="homegroups_bot")
