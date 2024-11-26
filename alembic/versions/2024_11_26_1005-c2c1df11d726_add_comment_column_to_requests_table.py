from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c2c1df11d726"
down_revision: Union[str, None] = "5e24c28e0800"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "requests",
        sa.Column("comment", sa.String(), nullable=True),
        schema="homegroups_bot",
    )


def downgrade() -> None:
    op.drop_column("requests", "comment", schema="homegroups_bot")
