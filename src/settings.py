from pydantic import BaseSettings
from pydantic import Field


class Server(BaseSettings):
    host: str = Field('localhost', env='METEO_APP_HOST')
    port: int = Field(5000, env='METEO_APP_PORT')
    
    
class OpenWeather(BaseSettings):
    host: str = Field('http://api.openweathermap.org', env='OPEN_WEATHER_HOST')
    apy_key: str = Field('secret', env='OPEN_WEATHER_APY_KEY')


class Storage(BaseSettings):
    host: str = Field('localhost', env='METEO_APP_PORT_REDIS_HOST')
    port: str = Field(6379, env='METEO_APP_PORT_REDIS_PORT')


class Settings(BaseSettings):
    server: Server = Server()
    open_weather: OpenWeather = OpenWeather()
    storage: Storage = Storage()


settings = Settings()
