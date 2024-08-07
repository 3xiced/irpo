from loguru import logger

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .user.models import LoginUser
from .user.controllers import (
    get_user,
    is_device_blocked,
    add_device,
    is_device_associated,
    add_user_device_association
)


async def authenticate_user(
    session: AsyncSession, user_schema: LoginUser
) -> None:
    _is_device_blocked: bool | None = await is_device_blocked(session, user_schema.device_sn)
    # Если устройства не существует, добавляем в таблицу devices
    if _is_device_blocked is None:
        logger.info(f"device='{user_schema.device_sn}' does not exist, creating...")
        await add_device(session, user_schema.device_sn)
        logger.info(f"device='{user_schema.device_sn}' created")

    # Устройство существует и заблокированно
    if _is_device_blocked == True:
        logger.info(f"device='{user_schema.device_sn}' is blocked")
        raise HTTPException(403, "blocked")

    user_db = await get_user(session, user_schema.login)
    if user_db is None:
        raise HTTPException(404, "user not found")

    if not (user_schema.password == str(user_db["password"])):
        raise HTTPException(400, "user password incorrect")

    if (user_db["is_blocked"] == True):
        logger.info(f"user='{user_schema.login}' is blocked")
        raise HTTPException(403, "blocked")

    # - Если пользователь существует, проверяем, закреплено ли за ним уже какое-то устройство
    user_device = await is_device_associated(session, user_schema.login)

    # --- Если незакреплено, устанавливаем как активное, пропускаем
    if user_device is None:
        await add_user_device_association(session, user_schema.login, user_schema.device_sn)
        return

    # --- Если закреплено, не совпадает с текущим, 409 logged in on other device
    if user_device != user_schema.device_sn.replace("\u0000", ""):
        logger.info(f'user_device="{user_device}"'
                    f' schema.device_sn="{user_schema.device_sn}"')
        raise HTTPException(409, "logged in on other device")
