from fastapi import HTTPException

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from datetime import datetime

from .models import RegisterUser

from ...external.postgres import User, UserInfo


async def create_user(session: AsyncSession, user_schema: RegisterUser) -> None:
    model_dump = user_schema.model_dump()
    info = model_dump.pop("info")

    user_model = User(**model_dump)
    user_model.info = UserInfo(
        device_sn=info["device_sn"],
        active = True,
        logged = False,
        last_login = datetime.utcnow()
    )

    session.add(user_model)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(409, "user_name or email already exists")

    await session.refresh(user_model)


async def get_user(session: AsyncSession, login: str) -> dict | None:
    result = await session.execute(
        select(User)
        .where(or_(User.login == login, User.login == login))
        .options(selectinload(User.info))
    )
    result = result.scalar_one_or_none()
    return result.__dict__ if result is not None else None

