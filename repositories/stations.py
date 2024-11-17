from sqlalchemy import select

from bot.titles import MCK_CALLBACK
from config.db import connection
from entities import Group
from entities import Transport
from entities import GroupStation
from entities import Line
from entities import Station

types = ["Молодежные до 25", "Молодежные после 25"]


async def select_stations_by_line(line_callback, age_group):
    async with connection.session() as session:
        async with session.begin():
            rows = await session.execute(
                select(Station)
                .join(Line, Line.id == Station.line_id)
                .join(GroupStation, GroupStation.station_id == Station.id)
                .join(Group, Group.id == GroupStation.group_id)
                .join(Transport, Transport.id == Station.transport_id)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Line.callback_data == line_callback)
                .where(Group.age.in_(types) if age_group == "young" else Group.age.notin_(types))
                .order_by(Station.title)
            )
            result = rows.unique().scalars().all()
            return result


async def select_stations_by_mck(age_group):
    async with connection.session() as session:
        async with session.begin():
            rows = await session.execute(
                select(Station)
                .join(GroupStation, GroupStation.station_id == Station.id)
                .join(Group, Group.id == GroupStation.group_id)
                .join(Transport, Transport.id == Station.transport_id)
                .where(Transport.callback_data == MCK_CALLBACK)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Group.age.in_(types) if age_group == "young" else Group.age.notin_(types))
                .order_by(Station.title)
                .distinct()
            )
            result = rows.scalars().all()
            return result
