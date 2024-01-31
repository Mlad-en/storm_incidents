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
    cast_types = ["count_building_year", "count_vnl_locs", "avg_building_year", "predictions"]
    amsterdam_gdf[cast_types] = amsterdam_gdf[cast_types].fillna(0).astype(int)

    def style_function(feature):
        prediction = feature["properties"]["predictions"]
        fill_opacity = 0.5 if prediction == 1 else 0  # Adjust the fillOpacity for red areas
        color = "red" if prediction == 1 else "none"
        return {"fillColor": color, "color": "black", "weight": 1, "fillOpacity": fill_opacity}

    folium.GeoJson(
        amsterdam_gdf,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['grid_id', 'avg_building_year', 'predictions'], labels=True, sticky=True)
    ).add_to(amsterdam_map)

    return amsterdam_map



def weather_input():
    with st.form("Weather Information") as form:
        weather_main = st.selectbox(
            'What is the weather description?',
            ("Clear", "Thunderstorm", "Fog", "Smoke", "Snow", "Rain", "Mist", "Drizzle", "Clouds"))
        temperature = st.slider('What is the temperature?', -30, 50, 1)
        min_temperature = st.slider('What is the minimum temperature?', -30, 50, 1)
        max_temperature = st.slider('What is the maximum temperature?', -30, 50, 1)
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
                    "avg_temp": [temperature],
                    "avg_temp_min": [min_temperature],
                    "avg_wind_speed": [wind_speed],
                    "avg_wind_deg": [wind_degree],
                    "avg_wind_gust": [wind_gust],
                    "avg_rain_1h": [rain_1h],
                    "avg_snow_1h": [snow_1h],
                    "avg_temp_max": [max_temperature],
                    "dt_iso": [0],
                    "count_incidents": [0],
                    "weather_main_priority": [0]
                }
            )

        else:
            return form


GRID = load_grid_data()
BUILDINGS = load_buildings()
MODEL = load_model()
GEOGRAPHY = full_geography()
GEOGRAPHY = GEOGRAPHY.merge(BUILDINGS, on="grid_id", how="left")

def real_life_weather():
    st.title("Real Life Weather")

    # Create a form with only the submit button in the sidebar
    with st.sidebar.form("Weather Information"):
        # Submit button
        submitted = st.form_submit_button("Submit")

        # Process the form data if the submit button is clicked
        if submitted:
            # Do something when the form is submitted
            st.write("Form submitted!")

    # Additional content for the "Real Life Weather" page
    st.write("Add your content for Real Life Weather here.")

def explanation():
    st.title("Explanation")
    st.write("Add your content for Explanation here.")

def main():
    if check_password():
        sns.set_theme()
        DATA = None

        # Sidebar navigation
        page = st.sidebar.selectbox("Select a page", ["Prediction Map", "Real Life Weather", "Explanation"])

        if page == "Prediction Map":
            # Weather input in the left control panel
            with st.sidebar:
                st.header("Weather Information")
                weather_info = weather_input()

            # Display map if weather_info is available
            if isinstance(weather_info, pd.DataFrame):
                DATA = GRID.merge(weather_info, how='cross')
                predictions = MODEL.predict(DATA)
                DATA.loc[:, "predictions"] = predictions
                DATA = GEOGRAPHY.merge(DATA, on="grid_id")

                if isinstance(DATA, pd.DataFrame):
                    # Title for the Prediction Map page
                    st.title("Storm Incidents Prediction")

                    amsterdam_map = create_amsterdam_map(
                        DATA[
                            ["geometry",
                             "count_building_year",
                             "count_vnl_locs",
                             "avg_building_year",
                             "predictions",
                             'grid_id']
                        ]
                    )
                    st.markdown(folium_static(amsterdam_map, width=1000, height=800), unsafe_allow_html=True)
        elif page == "Real Life Weather":
            real_life_weather()
        elif page == "Explanation":
            explanation()

if __name__ == '__main__':
    main()