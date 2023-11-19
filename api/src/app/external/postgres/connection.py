from loguru import logger
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from ...settings import settings

base = declarative_base()
url = URL.create(
    drivername="postgresql+asyncpg",
    host=settings.db_host,
    port=settings.db_port,
    username=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
)
engine = create_async_engine(url)
