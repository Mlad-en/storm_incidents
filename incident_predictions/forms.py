from django import forms


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
        ("Squall", 'Squall'),
    )

    temp = forms.FloatField(min_value=-50, max_value=50)
    temp_min = forms.FloatField(min_value=-50, max_value=50)
    temp_max = forms.FloatField(min_value=-50, max_value=50)
    humidity = forms.IntegerField(min_value=0, max_value=100)
    wind_speed = forms.IntegerField(min_value=0, max_value=200)
    wind_deg = forms.IntegerField(min_value=0, max_value=360)
    wind_gust = forms.FloatField(min_value=0, max_value=200)
    rain_1h = forms.FloatField(min_value=0, max_value=100)
    rain_3h = forms.FloatField(min_value=0, max_value=100)
    snow_1h = forms.FloatField(min_value=0, max_value=100)
    weather_main = forms.ChoiceField(choices=WEATHER_MAIN_CHOICES)
