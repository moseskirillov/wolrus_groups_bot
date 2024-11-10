from sqlalchemy import select
from sqlalchemy.orm import joinedload

from config.db import connection
from entities import RegionalLeader


async def get_regional_leader_by_telegram_id(regional_leader_id: int):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(RegionalLeader)
                .where(RegionalLeader.id == regional_leader_id)
                .options(joinedload(RegionalLeader.user))
            )
            return row.scalar_one_or_none()
