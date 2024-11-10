from datetime import datetime

from sqlalchemy import insert
from sqlalchemy import select

from config.db import connection
from entities import User


async def create_or_update_user(first_name: str, last_name: str, telegram_id: str, telegram_login: str):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(User)
                .where(User.telegram_id == telegram_id))
            user = row.scalar_one_or_none()
            if user:
                user.last_login = datetime.now()
            else:
                await session.execute(
                    insert(User),
                    [
                        {
                            "first_name": first_name,
                            "last_name": last_name,
                            "telegram_login": telegram_login,
                            "telegram_id": telegram_id,
                            "created_at": datetime.now(),
                            "updated_at": datetime.now(),
                            "last_login": datetime.now()
                        }
                    ]
                )


async def update_user_phone(telegram_id: str, phone_number: str):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(User)
                .where(User.telegram_id == telegram_id))
            user = row.scalar_one_or_none()
            if user:
                user.phone = phone_number
                user.updated_at = datetime.now()


async def get_user_by_telegram_id(telegram_id: str):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(User)
                .where(User.telegram_id == telegram_id)
            )
            return row.scalar_one_or_none()
