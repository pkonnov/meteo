from copy import deepcopy
from typing import Dict, List, Union, Optional
import httpx
from httpx import Timeout
from pydantic.main import BaseModel


class SomethingResponse(BaseModel):
    status_code: int
    text: str


class MinutelyItem(BaseModel):
    dt: int
    precipitation: int


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class HourlyItem(BaseModel):
    dt: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: Optional[float]
    weather: List[WeatherItem]
    pop: Optional[int]


class Temp(BaseModel):
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


class FeelsLike(BaseModel):
    day: float
    night: float
    eve: float
    morn: float


class WeatherItem1(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class DailyItem(BaseModel):
    dt: int
    sunrise: int
    sunset: int
    moonrise: int
    moonset: int
    moon_phase: float
    temp: Temp
    feels_like: FeelsLike
    pressure: int
    humidity: int
    dew_point: float
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[WeatherItem1]
    clouds: int
    pop: float
    uvi: float
    snow: Optional[float] = None


class WeatherResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    minutely: Optional[List[MinutelyItem]]
    hourly: Optional[List[HourlyItem]]
    daily: Optional[List[DailyItem]]
    current: Optional[HourlyItem]


class GeoObj(BaseModel):
    name: str
    lat: float
    lon: float


class GeoResponse(BaseModel):
    items: List[GeoObj]


class OpenWeatherClient:

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 5,
        headers: Dict[str, str] = None,
    ):
        self.client = httpx.AsyncClient(timeout=Timeout(timeout))
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
        }
        if headers:
            self.headers.update(headers)
        self.params = {
           'appid': self.api_key,
           'lang': 'ru',
        }

    async def get_weather(self, lat: float, lon: float, units, dt: Optional[str] = None):
        url = self._get_url('/data/2.5/onecall')
        # url = self._get_url('/data/2.5/forecast')
        params = deepcopy(self.params)
        params.update(
            lat=lat,
            lon=lon,
            units=units
        )

        try:
            response = await self.client.get(url, params=params)
        except Exception:
            raise

        if response.status_code != 200:
            return SomethingResponse(status_code=response.status_code, text=response.text)

        return WeatherResponse.parse_obj(response.json())

    async def get_geodata(self, country_code: str, city_name: str) -> Union[GeoResponse, SomethingResponse]:
        url = self._get_url('/geo/1.0/direct')
        params = deepcopy(self.params)
        params.update(q=f'{city_name},{country_code}')

        try:
            response = await self.client.get(url, params=params)
        except Exception:
            raise

        if response.status_code != 200:
            return SomethingResponse(status_code=response.status_code, text=response.text)

        return GeoResponse(items=[GeoObj.parse_obj(item) for item in response.json()])

    def _get_url(self, path: str) -> str:
        return f'{self.base_url}{path}'
