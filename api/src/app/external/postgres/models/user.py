import uuid

from sqlalchemy import Column, ForeignKey, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..connection import base


class UserInfo(base):
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    last_login = Column(Date)
    device_sn = Column(String)
    active = Column(Boolean)
    logged = Column(Boolean)


class User(base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)

    info: UserInfo = relationship("UserInfo")
