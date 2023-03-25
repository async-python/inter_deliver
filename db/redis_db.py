from typing import Optional

from aioredis import Redis

rdb: Optional[Redis] = None


# Dependency
async def get_redis() -> Redis:
    return rdb
