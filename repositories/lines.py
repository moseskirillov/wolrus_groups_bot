from sqlalchemy import select

from bot.titles import TYPES
from config.db import connection
from entities import Group
from entities import GroupStation
from entities import Line
from entities import Station
from entities import Transport


async def select_available_metro_lines(transport_type, age_group):
    async with connection.session() as session:
        async with session.begin():
            rows = await session.execute(
                select(Line)
                .join(Station, Station.line_id == Line.id)
                .join(Transport, Transport.id == Station.transport_id)
                .join(GroupStation, GroupStation.station_id == Station.id)
                .join(Group, Group.id == GroupStation.group_id)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Group.age.in_(TYPES) if age_group == "young" else Group.age.notin_(TYPES))
                .where(Transport.callback_data == transport_type)
                .order_by(Line.color)
                .distinct()
            )
            result = rows.scalars().all()
            return result
