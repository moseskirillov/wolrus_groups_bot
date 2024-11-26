from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.orm import contains_eager, selectinload

from bot.titles import TYPES
from bot.wrappers import check_user_admin
from config.db import connection
from entities import Request, Group, GroupLeader, User


async def create_request(user_id: int, group_id: int):
    async with connection.session() as session:
        async with session.begin():
            await session.execute(
                insert(Request),
                [
                    {
                        "user_id": user_id,
                        "group_id": group_id,
                        "date": datetime.now(),
                    }
                ],
            )


async def get_request_by_id(request_id):
    async with connection.session() as session:
        async with session.begin():
            row = await session.execute(
                select(Request)
                .where(Request.id == int(request_id))
                .where(Request.is_processed == False)
            )
            result = row.unique().scalar_one_or_none()
            return result


async def update_request_by_id(request_id, text):
    async with connection.session() as session:
        async with session.begin():
            await session.execute(
                update(Request)
                .where(Request.id == int(request_id))
                .where(Request.is_processed == False)
                .values(comment=text, is_processed=True, process_date=datetime.now())
            )


async def get_requests(age_group="adult"):
    async with connection.session() as session:
        async with session.begin():
            rows = await session.execute(
                select(Request)
                .where(Request.is_processed == False)
                .join(Group, Group.id == Request.group_id)
                .join(GroupLeader, Group.leader_id == GroupLeader.id)
                .join(User, GroupLeader.user_id == User.id)
                .where(
                    Group.age.in_(TYPES)
                    if age_group == "young"
                    else Group.age.notin_(TYPES)
                )
                .options(
                    contains_eager(Request.group)
                    .contains_eager(Group.leader)
                    .contains_eager(GroupLeader.user),
                    selectinload(Request.user),
                )
            )
            result = rows.unique().scalars().all()
            return result
