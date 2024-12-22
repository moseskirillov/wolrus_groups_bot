from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "99985e9f19ab"
down_revision: Union[str, None] = "9161100c313e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "requests",
        sa.Column(
            "feedback_requested",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        schema="homegroups_bot",
    )


def downgrade() -> None:
    op.drop_column("requests", "feedback_requested", schema="homegroups_bot")
