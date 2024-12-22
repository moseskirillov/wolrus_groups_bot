from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "990d559398bf"
down_revision: Union[str, None] = "99985e9f19ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "requests",
        sa.Column(
            "feedback",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        schema="homegroups_bot",
    ),
    op.add_column(
        "requests",
        sa.Column(
            "feedback_date",
            sa.TIMESTAMP(),
            nullable=True
        ),
        schema="homegroups_bot",
    )


def downgrade() -> None:
    op.drop_column("requests", "feedback", schema="homegroups_bot")
    op.drop_column("feedback_date", "feedback", schema="homegroups_bot")
