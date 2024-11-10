from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from entities import Base
from entities.transports import Transport


class Station(Base):
    __tablename__ = "stations"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    callback_data: Mapped[str] = mapped_column(String(length=255), nullable=False)
    transport: Mapped["Transport"] = relationship("Transport")
    transport_id: Mapped[str] = mapped_column(ForeignKey("transports.id"), nullable=False)
    line_id: Mapped[str] = mapped_column(ForeignKey("lines.id"), nullable=True)
