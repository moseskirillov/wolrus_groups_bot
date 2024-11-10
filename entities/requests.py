from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities import Base
from entities import Group
from entities import User


class Request(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", lazy="joined")
    date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Group"] = relationship("Group", lazy="joined")
