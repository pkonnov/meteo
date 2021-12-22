from collections import Callable
from typing import Awaitable, TypeVar, Type, Optional, Any

import aioredis
from aioredis import Redis
from orjson import orjson
from pydantic.main import BaseModel

from settings import settings
from utils import default


async def get_conn():
    return await aioredis.from_url(
        f'redis://{settings.storage.host}:{settings.storage.port}',
    )


T = TypeVar("T", bound=BaseModel)


class Storage:

    get_conn: Callable[..., Awaitable[Redis]] = get_conn

    @classmethod
    async def get_data_by_key(cls, key: str, object_type: Type[T]) -> T:
        conn = await get_conn()
        raw_data = await conn.get(key)
        return object_type.parse_raw(raw_data)

    @classmethod
    async def set_data_by_key(cls, key: str, data_obj: T, expire: Optional[int] = None) -> Any:
        conn = await get_conn()
        deserialized_data = orjson.dumps(data_obj.dict(), default=default)
        return await conn.set(key, deserialized_data, ex=expire)

    @classmethod
    async def exists_key(cls, key: str) -> bool:
        conn = await get_conn()
        return bool(await conn.exists(key))
