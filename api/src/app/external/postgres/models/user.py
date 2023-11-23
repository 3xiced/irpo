from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import base


class Device(base):
    __tablename__ = "devices"

    sn = Column(String, primary_key=True)
    is_blocked = Column(Boolean, default=False)


class User(base):
    __tablename__ = "users"

    login = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String, unique=True)
    is_blocked = Column(Boolean)  # Статус пользователя - заплокирована ли учетка


class UserDevice(base):
    __tablename__ = "user_device"

    user_login: Mapped[str] = mapped_column(ForeignKey("users.login"), primary_key=True)
    device_sn: Mapped[str] = mapped_column(ForeignKey("devices.sn"), primary_key=True)
