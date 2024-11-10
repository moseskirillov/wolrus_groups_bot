from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from entities.base import Base


class GroupDay(Base):
    __tablename__ = "groups_days"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    day_id: Mapped[int] = mapped_column(ForeignKey("days.id"), nullable=False)
