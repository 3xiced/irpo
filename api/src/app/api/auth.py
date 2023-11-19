from loguru import logger

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .user.models import LoginUser
from .user.controllers import get_user


async def authenticate_user(
    session: AsyncSession, user_schema: LoginUser
) -> None:
    user_db = await get_user(session, user_schema.login)
    if user_db is None:
        raise HTTPException(404, "user not found")

    if not (user_schema.password == str(user_db["password"])):
        raise HTTPException(400, "user password incorrect")
