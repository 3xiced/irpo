from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .models import (
    BlockUser,
    RegisterUser,
    LoginUser,
    ErrorMessage,
)

from ...external.postgres import get_session
from .controllers import get_user, create_user, block_user
from ..auth import (
    authenticate_user,
)

user_router: APIRouter = APIRouter(
    prefix="/api",
    tags=["User"],
    responses={404: {"description": "User not found", "model": ErrorMessage}},
)


@user_router.post(
    path="/user",
    name="Create user",
    response_model=None,
    status_code=204,
    responses={
        409: {"description": "User already exists", "model": ErrorMessage},
    },
)
async def registration(
    user_schema: RegisterUser, session: AsyncSession = Depends(get_session)
) -> None:
    user_db = await get_user(session, user_schema.login)
    if user_db is not None:
        raise HTTPException(409, "user already exists")

    await create_user(session, user_schema)


@user_router.post(
    path="/user/auth",
    name="auth",
    response_model=None,
    status_code=204,
    responses={
        400: {"description": "User password incorrect", "model": ErrorMessage},
    },
)
async def login(
    user_schema: LoginUser,
    session: AsyncSession = Depends(get_session),
) -> None:
    await authenticate_user(session, user_schema)


@user_router.post(
    path="/user/block",
    name="block",
    response_model=None,
    status_code=204,
    responses={
        400: {"description": "User password incorrect", "model": ErrorMessage},
    },
)
async def block(
    data: BlockUser,
    session: AsyncSession = Depends(get_session),
) -> None:
    await block_user(session, data.device_sn)
