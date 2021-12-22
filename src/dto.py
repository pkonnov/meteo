from pydantic.main import BaseModel


class WeatherDTO(BaseModel):
    temp: float
    feels_like: float
    wind_speed: float
    weather_desc: str
