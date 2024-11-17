from sqlalchemy import select

from config.db import connection
from entities import District
from entities import Group

types = ["Молодежные до 25", "Молодежные после 25"]


async def select_mo_districts(age_group):
    async with connection.session() as session:
        async with session.begin():
            main_query = (
                select(District)
                .join(Group, Group.district_id == District.id)
                .where(District.is_mo == True)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Group.age.in_(types) if age_group == "young" else Group.age.notin_(types))
                .order_by(District.title)
            )
            rows = await session.execute(main_query)
            result = rows.unique().scalars().all()
            return result
