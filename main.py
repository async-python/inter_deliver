import aioredis
from aioredis import Redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from api.v1 import deliver_api
from core.config import AppSettings
from core.logger import init_logging
from db import redis_db
from exceptions.api_exception import ApiException

settings = AppSettings()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
init_logging()
app.include_router(deliver_api.router, prefix='/api/v1',
                   tags=['International Delivery Api'])

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


@app.exception_handler(ApiException)
async def unicorn_exception_handler(request: Request, exc: ApiException):
    status_code = exc.__dict__['status_code']
    content = exc.__dict__['name']
    return ORJSONResponse(
        status_code=status_code,
        content=content,
    )


@app.on_event('startup')
async def startup():
    redis_db.rdb = Redis(host=settings.redis_host,
                         port=settings.redis_port,
                         password=settings.redis_password,
                         decode_responses=True,
                         db=settings.redis_base)
    redis = aioredis.from_url(settings.sync_redis_url,
                              encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@app.on_event('shutdown')
async def shutdown():
    await redis_db.rdb.close()
