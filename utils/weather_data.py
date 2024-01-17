import datetime
from os.path import exists
from pathlib import Path

import numpy as np
import pandas as pd
from pydantic import BaseModel


def convert_to_utc_datetime(dt_str):
    parts = dt_str.split(" +")
    datetime_str = parts[0]
    dt = pd.to_datetime(datetime_str, format="%Y-%m-%d %H:%M:%S")
    return dt


class HistoricalDataEnglishColumns:
    dt = "dt"
    dt_iso = "dt_iso"
    timezone = "timezone"
    city_name = "city_name"
    latitude = "lat"
    longitude = "lon"
    temp = "temp"
    visibility = "visibility"
    dew_point = "dew_point"
    feels_like = "feels_like"
    temp_min = "temp_min"
    temp_max = "temp_max"
    pressure = "pressure"
    sea_level = "sea_level"
    grnd_level = "grnd_level"
    humidity = "humidity"
    wind_speed = "wind_speed"
    wind_deg = "wind_deg"
    wind_gust = "wind_gust"
    rain_1h = "rain_1h"
    rain_3h = "rain_3h"
    snow_1h = "snow_1h"
    snow_3h = "snow_3h"
    clouds_all = "clouds_all"
    weather_id = "weather_id"
    weather_main = "weather_main"
    weather_description = "weather_description"
    weather_icon = "weather_icon"

    @classmethod
    def get_column_types(cls):
        return {
            cls.timezone: "category",
            cls.city_name: "category",
            cls.latitude: "category",
            cls.longitude: "category",
            cls.pressure: np.int16,
            cls.humidity: np.int16,
            cls.wind_speed: np.int16,
            cls.wind_deg: np.int16,
            cls.clouds_all: np.int16,
            cls.weather_id: np.int16,
            cls.weather_main: "category",
        }


class SourceWeatherData:

    def __init__(self):
        files_dir = Path(__file__).parents[1] / "files/historical_weather_amsterdam.csv"
        assert exists(files_dir)
        self.dataframe = pd.read_csv(files_dir)

    def clean_data(self):

        dataframe = self.dataframe.dropna(how="all", axis=1)
        fill_missing = [
            HistoricalDataEnglishColumns.wind_gust,
            HistoricalDataEnglishColumns.rain_1h,
            HistoricalDataEnglishColumns.rain_3h,
            HistoricalDataEnglishColumns.snow_1h,
            HistoricalDataEnglishColumns.dew_point,
        ]
        dataframe = dataframe.astype(HistoricalDataEnglishColumns.get_column_types())
        dataframe.loc[:, fill_missing] = dataframe[fill_missing].fillna(0)
        dataframe = dataframe.drop(
            [
                HistoricalDataEnglishColumns.dt,
                HistoricalDataEnglishColumns.timezone,
                HistoricalDataEnglishColumns.city_name,
                HistoricalDataEnglishColumns.weather_icon,
                HistoricalDataEnglishColumns.weather_description,
                HistoricalDataEnglishColumns.weather_id,
                HistoricalDataEnglishColumns.latitude,
                HistoricalDataEnglishColumns.longitude,
                HistoricalDataEnglishColumns.visibility,
                HistoricalDataEnglishColumns.clouds_all
            ],
            axis=1,
        )
        dataframe[HistoricalDataEnglishColumns.dt_iso] = dataframe[
            HistoricalDataEnglishColumns.dt_iso
        ].apply(convert_to_utc_datetime)

        self.dataframe = dataframe

        return self


class WeatherDataValidationModel(BaseModel):

    dt_iso: datetime.datetime
    temp: float
    dew_point: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    wind_speed: int
    wind_deg: int
    wind_gust: float
    rain_1h: float
    rain_3h: float
    snow_1h: float
    weather_main: str
