from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from entities.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    phone: Mapped[str] = mapped_column(String(length=255), nullable=True)
    telegram_login: Mapped[str] = mapped_column(String(length=255), nullable=True, unique=True)
    telegram_id: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_youth_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
