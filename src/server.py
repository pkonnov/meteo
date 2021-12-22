from typing import Any

import orjson
import uvicorn
from fastapi import FastAPI

from routes import get_routers
from settings import settings


def install_uvicorn_server(title, http_host, http_port) -> uvicorn.Server:
    app = FastAPI(title=title)

    config = uvicorn.Config(
        app,
        host=http_host,
        port=http_port,
    )
    uvicorn_server = uvicorn.Server(config=config)

    return uvicorn_server


def get_http_server() -> uvicorn.Server:
    uvicorn_server: uvicorn.Server = install_uvicorn_server(
        'meteo',
        settings.server.host,
        settings.server.port,
    )
    app: FastAPI = uvicorn_server.config.app

    for router in get_routers():
        app.include_router(router, tags=['meteo'])

    return uvicorn_server
