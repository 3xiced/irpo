from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):
    login: str
    password: str
    email: EmailStr


class LoginUser(BaseModel):
    login: str
    password: str
    device_sn: str


class BlockUser(BaseModel):
    device_sn: str


class ErrorMessage(BaseModel):
    detail: str
