from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities import Base
from entities.regional_leaders import RegionalLeader
from entities.users import User


class GroupLeader(Base):
    __tablename__ = "groups_leaders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User")
    regional_leader_id: Mapped[int] = mapped_column(ForeignKey("regional_leaders.id"), nullable=False)
    regional_leader: Mapped["RegionalLeader"] = relationship("RegionalLeader")
