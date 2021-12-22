from fastapi import APIRouter
from api import meteo


def get_routers() -> tuple[APIRouter, ...]:
    return (
        meteo.router,
    )
