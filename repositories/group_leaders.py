from sqlalchemy import select

from config.db import connection
from entities import GroupLeader, User


async def get_group_leader_by_telegram_id(telegram_id: str):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(GroupLeader)
                .where(User.telegram_id == telegram_id)
            )
            return row.scalar_one_or_none()
