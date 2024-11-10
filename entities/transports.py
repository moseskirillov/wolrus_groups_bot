from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from entities import Base


class Transport(Base):
    __tablename__ = "transports"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    callback_data: Mapped[str] = mapped_column(String(length=255), nullable=False)
