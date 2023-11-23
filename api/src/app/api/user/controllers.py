from fastapi import HTTPException

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from .models import RegisterUser

from ...external.postgres import User, Device, UserDevice


async def create_user(session: AsyncSession, user_schema: RegisterUser) -> None:
    model_dump = user_schema.model_dump()

    user_model = User(
        login=model_dump["login"],
        password=model_dump["password"],
        email=model_dump["email"],
        is_blocked=False,
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
    )
    result = result.scalar_one_or_none()
    return result.__dict__ if result is not None else None


async def is_device_blocked(session: AsyncSession, device_sn: str) -> bool | None:
    result = await session.execute(
        select(Device)
        .where(Device.sn == device_sn.replace("\u0000", ""))
    )
    result = result.scalar_one_or_none()
    return result.__dict__["is_blocked"] if result is not None else None


async def add_device(session: AsyncSession, device_sn: str) -> None:
    device_model = Device(
        sn=device_sn.replace("\u0000", ""),
        is_blocked=False
    )

    session.add(device_model)
    try:
        await session.commit()
    except IntegrityError:
        ...
    await session.refresh(device_model)


async def is_device_associated(session: AsyncSession, login: str) -> str | None:
    result = await session.execute(
        select(UserDevice)
        .where(UserDevice.user_login == login)
    )
    result = result.scalar_one_or_none()
    return result.__dict__["device_sn"] if result is not None else None


async def add_user_device_association(session: AsyncSession, login: str, device_sn: str) -> None:
    user_device_model = UserDevice(
        user_login=login,
        device_sn=device_sn.replace("\u0000", "")
    )

    session.add(user_device_model)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(409, "logged in on other device")
    await session.refresh(user_device_model)
