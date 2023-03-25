from abc import ABC, abstractmethod
from typing import Sequence, Type

from sqlalchemy import Row
from sqlalchemy.engine.result import _TP

from models.sql.sql_models import SqlBase


class AbstractSqlService(ABC):

    @abstractmethod
    async def insert(self, model: Type[SqlBase], data: dict) -> int:
        ...

    @abstractmethod
    async def fetchall(self, query) -> Sequence[Row[_TP]]:
        ...

    @abstractmethod
    async def get_models_all(self, model: Type[SqlBase]) -> Sequence[SqlBase]:
        ...

    @abstractmethod
    async def check_exists(self, model: Type[SqlBase], obj_id: int) -> bool:
        ...

    @abstractmethod
    async def get_model_by_id(
            self, model: Type[SqlBase], obj_id: int) -> Type[SqlBase]:
        ...
