from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from core.config import AppSettings

settings = AppSettings()

engine = create_async_engine(settings.mysql_url, echo=True)
async_session = async_sessionmaker(bind=engine, autoflush=False, future=True,
                                   expire_on_commit=False)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        await session.begin()
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(e)
