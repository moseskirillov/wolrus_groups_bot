from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from entities import Base


class District(Base):
    __tablename__ = "districts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    callback_data: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_mo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
