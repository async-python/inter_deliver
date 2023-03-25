from typing import Optional

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response


def secured_key_builder(
        func,
        namespace: Optional[str] = '',
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
    prefix = FastAPICache.get_prefix()
    user_id = request.session.get('user_id')
    cache_key = (f'{prefix}:{user_id}:{namespace}:{func.__module__}:'
                 f'{func.__name__}:{args}:{kwargs}')
    return cache_key
