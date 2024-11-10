from sqlalchemy import select

from config.db import connection
from entities import Transport


async def select_transports():
    async with connection.session() as session:
        async with session.begin():
            rows = await session.execute(select(Transport))
            result = rows.scalars().all()
            return result
