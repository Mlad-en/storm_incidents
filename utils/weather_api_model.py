import os
from json import JSONDecodeError
from typing import Any, Literal, Annotated

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator, ValidationError


class RainTypeInfo(BaseModel):
    last3_hours: Annotated[float, Field(alias="3h")] = 0


class WindInfo(BaseModel):
    speed: float
    deg: float
    gust: float


class WeatherInfo(BaseModel):
    id: int
    main: Literal[
        "Clear", "Thunderstorm", "Fog", "Smoke", "Haze", "Snow", "Rain", "Mist", "Drizzle", "Clouds", "Squall", 'Squall']
    description: str
    icon: str


class CloudsInfo(BaseModel):
    all: int


class MainInfo(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    sea_level: float
    grnd_level: float
    humidity: float
    temp_kf: float


class WeatherHourly(BaseModel):
    dt: int
    main: MainInfo
    weather: list[WeatherInfo]
    clouds: CloudsInfo
    wind: WindInfo
    visibility: int
    pop: float
    rain: Annotated[RainTypeInfo, Field(default=RainTypeInfo())]
    snow: Annotated[RainTypeInfo, Field(default=RainTypeInfo())]
    dt_txt: str

    @model_validator(mode="after")
    def validate_atts(self) -> "WeatherHourly":
        order_items = {
            'Clear': 1,
            'Haze': 2,
            'Mist': 2,
            'Smoke': 2,
            'Fog': 2,
            'Clouds': 3,
            'Drizzle': 3,
            'Rain': 4,
            'Squall': 5,
            'Snow': 5,
            'Thunderstorm': 6
        }

        self.weather.sort(key=lambda x: order_items.get(x.main, 0), reverse=True)

        return self


class WeatherApiModel(BaseModel):
    cod: str
    message: int
    cnt: int
    list: list[WeatherHourly]


class GetWeatherDataModel(BaseModel):

    model: WeatherApiModel | None = None
    status: str = "Not Called"

    def fetch_current_weather_data(self):
        load_dotenv()

        url = os.getenv("OPEN_WEATHER_URL")

        params = {
            "appid": os.getenv("OPEN_WEATHER_API_KEY"),
            "lat": os.getenv("OPEN_WEATHER_LATITUDE"),
            "lon": os.getenv("OPEN_WEATHER_LONGITUDE"),
            "units":"metric"
        }
        response = httpx.get(url, params=params)

        if response.status_code != 200:
            self.status = "Failed Api Call"
            return self

        try:
            data = response.json()
            self.model = WeatherApiModel(**data)
            self.status = "ok"
            return self

        except (ValidationError, JSONDecodeError) as e:
            self.status = "Validation Error"
            return self

    def get_initial_values(self):

        if self.status ==  "ok":
            initial_values = {
                'weather_main': self.model.list[0].weather[0].main,
                'rain_1h': self.model.list[0].rain.last3_hours,
                'rain_3h': self.model.list[0].rain.last3_hours,
                'snow_1h': self.model.list[0].snow.last3_hours,
                'wind_gust': self.model.list[0].wind.gust,
                'wind_deg': self.model.list[0].wind.deg,
                'wind_speed': self.model.list[0].wind.speed,
                'humidity': self.model.list[0].main.humidity,
                'temp': self.model.list[0].main.temp,
                'temp_min': self.model.list[0].main.temp_min,
                'temp_max': self.model.list[0].main.temp_max,
            }

        else:
            initial_values = {
                'weather_main': "Clear",
                'rain_1h': 0,
                'rain_3h': 0,
                'snow_1h': 0,
                'wind_gust': 0,
                'wind_deg': 0,
                'wind_speed': 0,
                'humidity': 0,
            }

        return initial_values
