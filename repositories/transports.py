from sqlalchemy import select

from bot.titles import TYPES
from config.db import connection
from entities import District
from entities import Group
from entities import GroupStation
from entities import Station
from entities import Transport


async def select_moscow_transports(age_group):
    async with connection.session() as session:
        async with session.begin():
            rows = await session.execute(
                select(Transport)
                .join(Station, Station.transport_id == Transport.id)
                .join(GroupStation, GroupStation.station_id == Station.id)
                .join(Group, Group.id == GroupStation.group_id)
                .join(District, District.id == Group.district_id)
                .where(District.is_mo == False)
                .where(
                    Group.age.in_(TYPES)
                    if age_group == "young"
                    else Group.age.notin_(TYPES)
                )
            )
            result = rows.unique().scalars().all()
            return result
