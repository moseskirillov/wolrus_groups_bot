from datetime import datetime

from sqlalchemy import insert

from config.db import connection
from entities import Request


async def create_request(user_id: int, group_id: int):
    async with connection.session() as session:
        async with session.begin():
            await session.execute(
                insert(Request),
                [{
                    'user_id': user_id,
                    'group_id': group_id,
                    'date': datetime.now(),
                }]
            )
