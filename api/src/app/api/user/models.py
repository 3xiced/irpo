from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    device_sn: str


class RegisterUser(BaseModel):
    login: str
    password: str
    email: EmailStr
    info: UserInfo


class LoginUser(BaseModel):
    login: str
    password: str
    info: UserInfo


class ErrorMessage(BaseModel):
    detail: str
