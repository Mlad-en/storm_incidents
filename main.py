import folium
from streamlit_folium import st_folium, folium_static

from configurations import configure_django

configure_django()

import joblib
import pandas as pd
import geopandas as gpd
import seaborn as sns
import streamlit as st
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate
from incident_predictions import database_views, models


application = get_wsgi_application()


def check_password():
    def password_entered():
        user = authenticate(
            username=st.session_state["username"], password=st.session_state["password"]
        )

        if user is not None:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        return True


@st.cache_data
def full_geography():
    amsterdam_grid = models.AmsterdamGridModel.objects.all().values()
    df = pd.DataFrame(list(amsterdam_grid))
    wkt = df.geometry.apply(lambda x: x.wkt)
    df = gpd.GeoDataFrame(df, crs=4326, geometry=gpd.GeoSeries.from_wkt(wkt))
    return df


@st.cache_data
def load_grid_data():
    data = database_views.EnvironmentMetricsGridWithIncidents.objects.all().values()
    return pd.DataFrame(list(data))


@st.cache_data
def load_buildings():
    buildings_locations = database_views.GridBuildingsVunerableLocations.objects.all().values()
    return pd.DataFrame(list(buildings_locations))


@st.cache_data
def load_model():
    filtered_models = models.PredictiveModels.objects.first()
    return joblib.load(filtered_models.file.path)


def create_amsterdam_map(amsterdam_gdf):
    amsterdam_map = folium.Map(location=[52.3676, 4.9041], zoom_start=12)
    cast_types = ["count", "count_vnl_locs", "avg_year", "predictions"]
    amsterdam_gdf[cast_types] = amsterdam_gdf[cast_types].fillna(0).astype(int)
    folium.GeoJson(
        amsterdam_gdf,
        tooltip=folium.features.GeoJsonTooltip(fields=['grid_id', 'avg_year', 'predictions'], labels=True, sticky=True)
    ).add_to(amsterdam_map)

    return amsterdam_map


def weather_input():
    with st.form("Weather Information") as form:
        weather_main = st.selectbox(
            'What is the weather description?',
            ("Clear", "Thunderstorm", "Fog", "Smoke", "Snow", "Rain", "Mist", "Drizzle", "Clouds"))
        temperature = st.slider('What is the temperature?', -30, 50, 1)
        min_temperature = st.slider('What is the minimum temperature?', -30, 50, 1)
        wind_speed = st.slider('What is the wind speed?', 0, 200, 1)
        wind_degree = st.slider('What is the wind degree?', 0, 360, 1)
        wind_gust = st.slider('What is the wind gust?', 0, 200, 1)
        rain_1h = st.slider('How much has it rained in the last hour?', 0, 200, 1)
        snow_1h = st.slider('How much has it snowed in the last hour?', 0, 200, 1)

        submitted = st.form_submit_button("Submit")
        if submitted:
            return pd.DataFrame(
                {
                    "weather_main": [weather_main],
                    "temp": [temperature],
                    "temp_min": [min_temperature],
                    "wind_speed": [wind_speed],
                    "wind_deg": [wind_degree],
                    "wind_gust": [wind_gust],
                    "rain_1h": [rain_1h],
                    "snow_1h": [snow_1h],
                    "rain_3h": [0],
                    "dew_point": [0],
                    "humidity": [0],
                    "feels_like": [0],
                    "pressure": [0],
                    "temp_max": [0],
                }
            )

        else:
            return form


GRID = load_grid_data()
BUILDINGS = load_buildings()
MODEL = load_model()
GEOGRAPHY = full_geography()
GEOGRAPHY = GEOGRAPHY.merge(BUILDINGS, on="grid_id", how="left")


if __name__ == '__main__':

    if check_password():
        sns.set_theme()
        DATA = None
        weather_info = weather_input()
        if isinstance(weather_info, pd.DataFrame):
            DATA = GRID.merge(weather_info, how='cross')
            predictions = MODEL.predict(DATA)
            DATA.loc[:, "predictions"] = predictions
            DATA = GEOGRAPHY.merge(DATA, on="grid_id")

        if isinstance(DATA, pd.DataFrame):
            amsterdam_map = create_amsterdam_map(DATA[["geometry", "count", "count_vnl_locs", "avg_year", "predictions", 'grid_id']])
            st.markdown(folium_static(amsterdam_map, width=1000, height=800), unsafe_allow_html=True)

