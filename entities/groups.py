from datetime import time
from typing import List

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import TIME
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from config.settings import settings
from entities import Day
from entities import District
from entities import GroupLeader
from entities.base import Base
from entities.stations import Station


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[time] = mapped_column(TIME, nullable=False)
    age: Mapped[str] = mapped_column(String(length=255), nullable=False)
    type: Mapped[str] = mapped_column(String(length=255), nullable=False)
    description: Mapped[str] = mapped_column(String(length=255), nullable=True)
    is_open: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_overflow: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_multi_day: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    leader_id: Mapped[int] = mapped_column(ForeignKey("groups_leaders.id"), nullable=False)
    leader: Mapped["GroupLeader"] = relationship("GroupLeader")
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)
    district: Mapped["District"] = relationship("District")
    days: Mapped[List[Day]] = relationship(secondary=f"{settings.db.tables_schema}.groups_days")
    stations: Mapped[List[Station]] = relationship(secondary=f"{settings.db.tables_schema}.groups_stations")
