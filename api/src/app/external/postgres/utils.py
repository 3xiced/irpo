from loguru import logger
from .connection import engine, base
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tables():
    async with engine.begin() as connection:
        logger.info('msg="creating tables..."')
        await connection.run_sync(base.metadata.create_all)
        logger.info('msg="tables created"')


async def drop_tables():
    async with engine.begin() as connection:
        logger.info('msg="droping tables..."')
        await connection.run_sync(base.metadata.drop_all)
        logger.info('msg="tables droped"')


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
