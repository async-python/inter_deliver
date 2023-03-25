from functools import lru_cache
from typing import Optional, Sequence, Type, Union
from uuid import UUID

from fastapi import Depends
from loguru import logger
from sqlalchemy import Row, select
from sqlalchemy.engine.result import _TP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings
from db.mysql_db import get_session
from models.sql.sql_models import SqlBase, TypeSql
from services.abstracts import AbstractSqlService

settings = AppSettings()


class SqlService(AbstractSqlService):

    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def insert(self, model: Type[SqlBase], data: dict) -> int:
        try:
            addition = model(**data)
            self.db.add(addition)
            await self.db.commit()
        except SQLAlchemyError as error:
            await self.db.rollback()
            logger.error(error)
            raise error
        else:
            await self.db.refresh(addition)
            return addition.id

    async def fetchall(self, query) -> Sequence[Row[_TP]]:
        response = await self.db.execute(query)
        return response.fetchall()

    async def get_models_all(self, model: Type[SqlBase]) -> Sequence[SqlBase]:
        stmt = select(model).order_by(model.id)
        response = await self.db.execute(stmt)
        return response.scalars().all()

    async def check_exists(
            self, model: Type[SqlBase], obj_id: Union[int, UUID]) -> bool:
        p_type = await self.db.get(TypeSql, obj_id)
        return p_type is not None

    async def get_model_by_id(self,
                              model: Type[SqlBase],
                              obj_id: int) -> Optional[Type[SqlBase]]:
        response = await self.db.get(model, obj_id)
        return response


@lru_cache()
def get_sql_service(
        session: AsyncSession = Depends(get_session)) -> SqlService:
    return SqlService(session)
