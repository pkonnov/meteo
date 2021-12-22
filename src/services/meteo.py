import datetime
import logging
from typing import Union

from clients.client_factory import OpenWeatherClientFactory
from clients.meteo import GeoResponse, WeatherResponse
from dto import WeatherDTO
from storage import Storage
from utils import get_hash_of

client = OpenWeatherClientFactory.get_client()
logger = logging.getLogger(__name__)


class OpenWeatherService:

    @classmethod
    async def get_weather(cls, country_code: str, city_name: str, date: datetime.date) -> Union[WeatherDTO]:
        _hash_req = get_hash_of({0: country_code, 1: city_name, 2: date})

        context_key = f'weather:{_hash_req}'
        if await Storage.exists_key(context_key):
            data_from_storage = await Storage.get_data_by_key(context_key, WeatherDTO)
            return data_from_storage

        resp_geo_data = await client.get_geodata(country_code, city_name)
        if not isinstance(resp_geo_data, GeoResponse) or not len(resp_geo_data.items):
            logger.error('Error at get geo data', extra={'resp': resp_geo_data})
            raise

        geo_data = resp_geo_data.items[0]
        resp_weather = await client.get_weather(geo_data.lat, geo_data.lon, 'metric')
        if not isinstance(resp_weather, WeatherResponse):
            logger.error('Error at get weather', extra={'resp': resp_weather.json()})
            raise

        if date > datetime.date.today():
            _weather_obj = next(filter(lambda el: datetime.date.fromtimestamp(el.dt) == date, resp_weather.daily), None)
            weather = WeatherDTO(temp=_weather_obj.temp.day, feels_like=_weather_obj.feels_like.day,
                                 wind_speed=_weather_obj.wind_speed, weather_desc=_weather_obj.weather[0].description)
        else:
            dt = datetime.datetime(year=date.year, month=date.month, day=date.day) + datetime.timedelta(hours=12)
            weather_obj = next(filter(lambda el: el.dt >= int(dt.strftime('%s')), resp_weather.hourly), None)
            weather = WeatherDTO(temp=weather_obj.temp, feels_like=weather_obj.feels_like, wind_speed=weather_obj.wind_speed,
                                 weather_desc=weather_obj.weather[0].description)

        await Storage.set_data_by_key(context_key, weather, 60)

        return weather
