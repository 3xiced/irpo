from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession


class UserInfo(BaseModel):
    device_sn: str


class RegisterUser(BaseModel):
    login: str
    email: EmailStr
    password: str
    info: UserInfo
    

class LoginUser(BaseModel):
    login: str
    password: str
    info: UserInfo


class UserSchema(BaseModel):
    id: UUID
    login: str
    email: str
    password: str
    settings: UserInfo
    session: AsyncSession
    

class ErrorMessage(BaseModel):
    detail: str
