import hashlib
from typing import Any, Dict

from pydantic.main import BaseModel
from starlette.responses import JSONResponse

import orjson


def default(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return obj.dict()
    raise TypeError


def serialize_to_bytes(content: Any) -> bytes:
    if isinstance(content, bytes):
        return content
    return orjson.dumps(content, option=orjson.OPT_PASSTHROUGH_DATETIME, default=default)


class MyORJSONResponse(JSONResponse):
    media_type = 'application/json'

    def render(self, content: Any) -> bytes:
        return serialize_to_bytes(content)


def get_hash_of(data: Dict) -> str:
    _hash = None
    for _, el in data.items():
        hash_str = f'{el}'.encode()
        if not _hash:
            _hash = hashlib.md5(hash_str)
            continue
        _hash.update(hash_str)
    return _hash.hexdigest()
