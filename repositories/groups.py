from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import selectinload

from bot.titles import TYPES
from config.db import connection
from entities import Group, District
from entities import GroupLeader
from entities import GroupStation
from entities import RegionalLeader
from entities import Station
from entities import User


async def select_groups_by_station(station_callback, age_group):
    async with connection.session() as session:
        async with session.begin():
            main_query = (
                select(Group)
                .join(GroupLeader, Group.leader_id == GroupLeader.id)
                .join(User, GroupLeader.user_id == User.id)
                .join(GroupStation, GroupStation.group_id == Group.id)
                .join(Station, GroupStation.station_id == Station.id)
                .join(District, Group.district_id == District.id)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Group.age.in_(TYPES) if age_group == "young" else Group.age.notin_(TYPES))
                .where(Station.callback_data == station_callback)
                .options(
                    contains_eager(Group.leader).contains_eager(GroupLeader.user),
                    contains_eager(Group.district),
                    selectinload(Group.days),
                    selectinload(Group.stations).joinedload(Station.transport)
                )
            )
            rows = await session.execute(main_query)
            result = rows.unique().scalars().all()
            return result


async def select_group_by_id(group_id):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(Group)
                .where(Group.id == int(group_id))
                .join(GroupLeader, Group.leader_id == GroupLeader.id)
                .join(RegionalLeader, GroupLeader.regional_leader_id == RegionalLeader.id)
                .join(User, GroupLeader.user_id == User.id)
                .options(contains_eager(Group.leader).contains_eager(GroupLeader.user))
            )
            result = row.unique().scalar_one_or_none()
            return result


async def select_online_groups(age_group):
    async with connection.session() as session:
        async with session.begin():
            main_query = (
                select(Group)
                .join(GroupLeader, Group.leader_id == GroupLeader.id)
                .join(User, GroupLeader.user_id == User.id)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Group.district_id == 22)
                .where(Group.age.in_(TYPES) if age_group == "young" else Group.age.notin_(TYPES))
                .where(1 == 1 if age_group == "young" else Group.district_id == 22)
                .order_by(Group.leader_id)
                .options(
                    contains_eager(Group.leader).contains_eager(GroupLeader.user),
                    selectinload(Group.days)
                )
            )
            rows = await session.execute(main_query)
            result = rows.unique().scalars().all()
            return result


async def select_groups_by_district(district_callback, age_type):
    async with connection.session() as session:
        async with session.begin():
            main_query = (
                select(Group)
                .join(GroupLeader, Group.leader_id == GroupLeader.id)
                .join(User, GroupLeader.user_id == User.id)
                .join(GroupStation, GroupStation.group_id == Group.id)
                .join(Station, GroupStation.station_id == Station.id)
                .join(District, Group.district_id == District.id)
                .where(Group.is_open)
                .where(Group.is_overflow == False)
                .where(Group.age.in_(TYPES) if age_type == "young" else Group.age.notin_(TYPES))
                .where(District.callback_data == district_callback)
                .options(
                    contains_eager(Group.leader).contains_eager(GroupLeader.user),
                    contains_eager(Group.district),
                    selectinload(Group.days),
                    selectinload(Group.stations).joinedload(Station.transport)
                )
            )
            rows = await session.execute(main_query)
            result = rows.unique().scalars().all()
            return result