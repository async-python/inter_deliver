from typing import Sequence
from uuid import UUID

from fastapi import Depends
from starlette import status

from exceptions.api_exception import ApiException
from models.entry.entry_models import PackageDb
from models.out.out_models import (PackageDetailFullOut, PackageDetailShortOut,
                                   PackageIdOut, TypesOut)
from models.sql.sql_models import PackageSql, TypeSql
from services.session_service import get_session_id
from services.sql_service import SqlService, get_sql_service
from utils.sql_queries import get_packages_query


class ApiController:

    def __init__(self, session_id: UUID, sql_service) -> None:
        self.sid = session_id
        self.sql_sv = sql_service

    async def add_package(self, package) -> PackageIdOut:
        type_check = await self.sql_sv.check_exists(
            TypeSql, package.type_id)
        if not type_check:
            raise ApiException(
                name=f'type_id: {package.type_id} don\'t exists',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        package_dict = package.dict()
        package_dict['session_id'] = self.sid
        response = PackageDb(**package_dict)
        pid = await self.sql_sv.insert(PackageSql, response.dict())
        return PackageIdOut(id=pid)

    async def get_packages(self, **kwargs):
        kwargs['session_id'] = self.sid
        query = get_packages_query(**kwargs)
        packages = await self.sql_sv.fetchall(query)
        return [PackageDetailFullOut(
            name=x.name,
            weight=x.weight,
            type_name=y,
            usd_price=x.usd_price,
            delivery_cost=x.cost) for x, y in packages]

    async def get_package_detail(self, package_id):
        package = await self.sql_sv.get_model_by_id(
            PackageSql, package_id)
        if not package:
            raise ApiException(
                name=f'package_id: {package_id} Not found',
                status_code=status.HTTP_404_NOT_FOUND)
        if package.session_id != self.sid:
            raise ApiException(
                name='Access forbidden',
                status_code=status.HTTP_403_FORBIDDEN)
        return PackageDetailShortOut(
            name=package.name,
            weight=package.weight,
            type=package.type_id,
            delivery_cost=package.cost if
            package.cost else 'not calculated')

    async def get_types(self):
        types: Sequence[TypeSql] = await self.sql_sv.get_models_all(TypeSql)
        return [TypesOut(**obj.as_dict()) for obj in types]


async def get_api_controller(session_id: UUID = Depends(get_session_id),
                             sql_sv: SqlService = Depends(get_sql_service)):
    return ApiController(session_id, sql_sv)
