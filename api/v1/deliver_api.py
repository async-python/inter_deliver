from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.params import Path
from fastapi_cache import JsonCoder
from fastapi_cache.decorator import cache

from api.v1.controller import ApiController, get_api_controller
from models.entry.entry_models import PackageEntry
from models.out.out_models import (PackageDetailFullOut, PackageDetailShortOut,
                                   PackageIdOut, TypesOut)
from utils.cache_utils import secured_key_builder
from utils.endpoint_params import (page_num_params, page_size_params,
                                   type_params)

router = APIRouter()


@router.post('/register', response_model=PackageIdOut)
async def register(package: PackageEntry,
                   controller: ApiController = Depends(
                       get_api_controller)):
    return await controller.add_package(package)


@router.get('/packages', response_model=list[PackageDetailFullOut])
@cache(expire=60, key_builder=secured_key_builder, coder=JsonCoder)
async def get_packages(page_number: int = Query(**page_num_params),
                       page_size: int = Query(**page_size_params),
                       type_id: Optional[int] = Query(**type_params),
                       cost_calculated: bool = Query(default=True),
                       controller: ApiController = Depends(
                           get_api_controller)):
    kwargs = {
        'page_number': page_number,
        'page_size': page_size,
        'type_id': type_id,
        'cost_calculated': cost_calculated
    }
    return await controller.get_packages(**kwargs)


@router.get('/package/detail/{package_id}',
            response_model=PackageDetailShortOut,
            responses={403: {'detail': 'Access forbidden'},
                       404: {'detail': 'Not found'}})
@cache(expire=60, key_builder=secured_key_builder, coder=JsonCoder)
async def get_package_detail(package_id: int = Path(title='ID'),
                             controller: ApiController = Depends(
                                 get_api_controller)):
    return await controller.get_package_detail(package_id)


@router.get('/types', response_model=list[TypesOut])
@cache(expire=60, coder=JsonCoder)
async def get_types(controller: ApiController = Depends(get_api_controller)):
    return await controller.get_types()
