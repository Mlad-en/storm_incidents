import pandas as pd
from django import forms

from incident_predictions import models


class WeatherDataForm(forms.Form):

    WEATHER_MAIN_CHOICES = (
        ("Clear", 'Clear'),
        ("Thunderstorm", 'Thunderstorm'),
        ("Fog", 'Fog'),
        ("Smoke", 'Smoke'),
        ("Haze", 'Haze'),
        ("Snow", 'Snow'),
        ("Rain", 'Rain'),
        ("Mist", 'Mist'),
        ("Drizzle", 'Drizzle'),
        ("Clouds", 'Clouds'),
    )

    temp = forms.FloatField(min_value=-50, max_value=50)
    temp_min = forms.FloatField(min_value=-50, max_value=50)
    wind_speed = forms.IntegerField(min_value=0, max_value=200)
    wind_deg = forms.IntegerField(min_value=0, max_value=360)
    wind_gust = forms.FloatField(min_value=0, max_value=200)
    rain_1h = forms.FloatField(min_value=0, max_value=100)
    snow_1h = forms.FloatField(min_value=0, max_value=100)
    weather_main = forms.ChoiceField(choices=WEATHER_MAIN_CHOICES)
    model = forms.CharField(max_length=100)

    def convert_to_dataframe(self):
        return pd.DataFrame(
            {
                "weather_main": [self.cleaned_data["weather_main"]],
                "temp": [self.cleaned_data["temp"]],
                "temp_min": [self.cleaned_data["temp_min"]],
                "temp_max": [self.cleaned_data["temp_min"]],
                "wind_speed": [self.cleaned_data["wind_speed"]],
                "wind_deg": [self.cleaned_data["wind_deg"]],
                "wind_gust": [self.cleaned_data["wind_gust"]],
                "rain_1h": [self.cleaned_data["rain_1h"]],
                "snow_1h": [self.cleaned_data["snow_1h"]],
                "rain_3h": [0],
                "dew_point": [0],
                "humidity": [0],
                "feels_like": [0],
                "pressure": [0],
            }
        )
