from sqlalchemy import select

from config.db import connection
from entities import Group
from entities import District


async def select_mo_districts():
    async with connection.session() as session:
        async with session.begin():
            main_query = (
                select(District)
                .join(Group, Group.district_id == District.id)
                .where(District.is_mo == True)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .order_by(District.title)
            )
            rows = await session.execute(main_query)
            result = rows.unique().scalars().all()
            return result
