from clients.meteo import OpenWeatherClient
from settings import settings


class OpenWeatherClientFactory:

    client: OpenWeatherClient = None

    @classmethod
    def get_client(cls) -> OpenWeatherClient:
        if not cls.client:
            cls.client = OpenWeatherClient(
                base_url=settings.open_weather.host,
                api_key=settings.open_weather.apy_key,
            )
        return cls.client
