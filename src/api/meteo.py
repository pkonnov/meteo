import datetime
import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from api.urls import APIUrls
from dto import WeatherDTO
from utils import MyORJSONResponse
from services.meteo import OpenWeatherService


router = APIRouter()
logger = logging.getLogger(__name__)


class QueryParams:
    def __init__(
        self,
        country_code: str = Query(..., description="Country code. Ex: ru, gbr, ua.."),
        city_name: str = Query(..., description="City name. Ex: kiev, saratov, london"),
        date: datetime.date = Query(..., description="Date. Ex: 2012-12-21"),
    ):
        self.country_code = country_code
        self.city_name = city_name
        self.date = date


@router.get(
    APIUrls.V1_WEATHER,
    response_model=WeatherDTO,
)
async def get_meteo_data(params: QueryParams = Depends()) -> MyORJSONResponse:
    try:
        weather = await OpenWeatherService.get_weather(params.country_code, params.city_name, params.date)
        return MyORJSONResponse(content=weather)
    except Exception as ex:
        logger.exception(ex)
        return MyORJSONResponse(content=str(ex), status_code=500)
