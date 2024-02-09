import logging

import folium
import matplotlib.pyplot as plt
import numpy as np
from streamlit_folium import folium_static
import plotly.graph_objs as go

from configurations import configure_django
from utils.weather_api_model import GetWeatherDataModel

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
            st.session_state["is_staff"] = user.is_staff
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
def service_area_data_loading():
    areas = models.ServiceAreasDataModel.objects.all().values()
    df = pd.DataFrame(list(areas))
    wkt = df.geometry.apply(lambda x: x.wkt)
    df = gpd.GeoDataFrame(df, crs="EPSG:28992", geometry=gpd.GeoSeries.from_wkt(wkt))
    df['geometry'] = df['geometry'].to_crs("EPSG:4326")
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


@st.cache_data
def load_tree_height():
    tree_height = database_views.CountTreeHeightView.objects.all().values()
    return pd.DataFrame(list(tree_height))


@st.cache_data
def load_building_pct():
    building_pct = database_views.building_pct_view.objects.all().values()
    return pd.DataFrame(list(building_pct))


def create_amsterdam_map(amsterdam_gdf, service_areas):
    amsterdam_map = folium.Map(location=[52.3676, 4.9041], zoom_start=12)
    cast_types = ["count_vnl_locs", "avg_building_year", "predictions"]
    amsterdam_gdf[cast_types] = amsterdam_gdf[cast_types].fillna(0).astype(int)

    def style_function(feature):
        prediction = feature["properties"]["predictions"]
        risk = feature["properties"]["risk"]

        # Define color and adjust opacity based on risk level
        color = "red"  # Set your desired color
        opacity = 0.1 + 0.2 * risk  # Adjust opacity based on risk level

        fill_opacity = opacity if prediction == 1 else 0
        return {"fillColor": color, "color": "black", "weight": 1, "fillOpacity": fill_opacity}

    child1 = folium.GeoJson(
        amsterdam_gdf,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(fields=
                                               ['grid_id', 'avg_building_year', 'count_vnl_locs', 'predictions',
                                                'risk'],
                                               labels=True, sticky=True)
    )
    child1.layer_name = '100x100 grid'

    child2 = folium.GeoJson(service_areas["geometry"])
    child2.layer_name = 'Service Areas'
    amsterdam_map.add_children(child2)
    amsterdam_map.add_children(child1)
    folium.LayerControl().add_to(amsterdam_map)

    additional_points = [
        [52.26295130210547, 4.76305970952781, 'Amsterdam-Amstelland Aalsmeer'],
        [52.358154952608366, 4.886063171988078, 'Amsterdam-Amstelland Dirk'],
        [52.37269177618045, 4.875679454794675, 'Amsterdam-Amstelland Hendrik'],
        [52.34889626306957, 4.9148519547932885, 'Amsterdam-Amstelland Willem'],
        [52.360585512082764, 4.929142910614777, 'Amsterdam-Amstelland Victor'],
        [52.370941181170124, 4.909433861091186, 'Amsterdam-Amstelland Nico'],
        [52.38489337929629, 4.863331900539332, 'Amsterdam-Amstelland Teunis'],
        [52.351081357219186, 4.84407584473503, 'Amsterdam-Amstelland Pieter'],
        [52.39745429734238, 4.953814914725336, 'Amsterdam-Amstelland Zebra'],
        [52.34355683224436, 4.965759303211002, 'Amsterdam-Amstelland Diemen'],
        [52.33466256068652, 4.939071060188342, 'Amsterdam-Amstelland Duivendrecht'],
        [52.41130841654537, 4.888752495088714, 'Amsterdam-Amstelland IJsbrand'],
        [52.31057376849848, 4.973208734677997, 'Amsterdam-Amstelland Anton'],
        [52.36983355801502, 4.8016570022515594, 'Amsterdam-Amstelland Osdorp']
    ]

    for point in additional_points:
        folium.Marker(location=[point[0], point[1]], popup=point[2], icon=folium.Icon(color='green')).add_to(
            amsterdam_map)

    return amsterdam_map


def weather_input():
    with st.form("Weather Information: ") as form:
        wind_speed = st.slider('What is the wind speed? (m/s)', 0, 35, 1)
        wind_degree = st.slider('What is the wind degree? (°)', 0, 360, 1)
        wind_gust = st.slider('What is the wind gust? (m/s)', 0, 35, 1)
        rain_1h = st.slider('How much has it rained in the last hour? (mm)', 0, 150, 1)
        snow_1h = st.slider('How much has it snowed in the last hour? (mm, liquid state)', 0, 150, 1)
        temperature = st.slider('What is the temperature? (°C)', -30, 50, 1)
        min_temperature = st.slider('What is the minimum temperature? (°C)', -30, 50, 1)
        max_temperature = st.slider('What is the maximum temperature? (°C)', -30, 50, 1)

        submitted = st.form_submit_button("Submit")
        if submitted:
            return pd.DataFrame(
                {
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
SERVICE_AREAS = service_area_data_loading()
MODEL = load_model()

TREE_HEIGHT = load_tree_height()
GEOGRAPHY = full_geography()
BUILDINGS_PCT = load_building_pct()
GEOGRAPHY = GEOGRAPHY.merge(BUILDINGS, on="grid_id", how="left")


def real_life_weather(data, include_cols):
    amsterdam_map = create_amsterdam_map(
        data[
            ["geometry",
             "count_vnl_locs",
             "avg_building_year",
             "predictions",
             'grid_id',
             "risk"
             ]
        ], SERVICE_AREAS
    )
    st.markdown(folium_static(amsterdam_map, width=1000, height=800), unsafe_allow_html=True)


def redirect_button(url: str, text: str= None, color="#FD504D"):
    st.markdown(
    f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )


def explanation():
    redirect_button("http://127.0.0.1:8000/admin/", "Admin")
    split_importance = MODEL.feature_importance(importance_type='split')
    gain_importance = MODEL.feature_importance(importance_type='gain')
    feature_names = MODEL.feature_name()


    split_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': split_importance})
    split_importance_df = split_importance_df.sort_values(by='Importance', ascending=False)

    gain_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': gain_importance})
    gain_importance_df = gain_importance_df.sort_values(by='Importance', ascending=False)

    st.title('Explainable AI')

    top_n = st.slider('Select the number of top features:', min_value=1, max_value=len(feature_names), value=10)

    st.write(
        """Consider information gain as a measure of a feature's impact on reducing model error -
         the higher the gain, the more significant the feature's contribution to model accuracy. 
         Split frequency indicates how often a feature is used to divide data in the model's decision trees,
          with higher frequencies suggesting a feature's consistent relevance across predictions."""
    )

    st.subheader(f'Top {top_n} Features by Gain Importance')
    gain_trace = go.Bar(
        x=gain_importance_df['Importance'].head(top_n),
        y=gain_importance_df['Feature'].head(top_n),
        orientation='h',
        name='Gain Importance'
    )
    gain_layout = go.Layout(
        yaxis=dict(title='Feature')
    )
    gain_fig = go.Figure(data=[gain_trace], layout=gain_layout)
    st.plotly_chart(gain_fig)

    st.subheader(f'Top {top_n} Features by Split Importance')
    split_trace = go.Bar(
        x=split_importance_df['Importance'].head(top_n),
        y=split_importance_df['Feature'].head(top_n),
        orientation='h',
        name='Split Importance'
    )

    split_layout = go.Layout(
        yaxis=dict(title='Feature')
    )
    split_fig = go.Figure(data=[split_trace], layout=split_layout)
    st.plotly_chart(split_fig)


def set_side_bar_options():
    if st.session_state.get('is_staff'):
        side_bar = ["Prediction Map", "Real Life Weather", "XAI"]
    else:
        side_bar = ["Real Life Weather", "Prediction Map"]

    return side_bar


def building_risk(value):
    if value < 8.2:
        return 1
    elif value < 33.9:
        return 2
    elif value < 51.9:
        return 3
    elif value < 68.3:
        return 4
    else:
        return 5


def vunerable_locations_risk(value):
    if value == 0:
        return 1
    elif value == 1:
        return 2
    elif value == 2:
        return 3
    elif value == 3:
        return 4
    else:
        return 5


def calculate_risk(dataframe):
    buildings_risk = dataframe["sum_area_building"].apply(building_risk)
    vunerable_locations = dataframe["count_vnl_locs"].apply(vunerable_locations_risk)
    predictions = dataframe["predictions"]
    risk = np.round(np.mean([buildings_risk, vunerable_locations], axis=0), 0)
    dataframe.loc[:, "risk"] = predictions * risk
    return dataframe


def combine_dataframes(weather_info):
    data = GRID.merge(weather_info, how='cross')
    exclude_cols = ["grid_id", "weather_main", "dt_iso", "count_incidents", "has_incident", "rain_3h"]
    include_cols = [col for col in data.columns if col not in exclude_cols]
    cast_cols = ['mean_tree_age', 'std_tree_age']
    data[cast_cols] = data[cast_cols].astype(float)

    return data, include_cols


def add_predictions(data, model, include_cols, decision_boundary):
    predictions = MODEL.predict(data[include_cols], num_iteration=MODEL.best_iteration)
    data.loc[:, "predictions"] = np.where(predictions < decision_boundary, 0, 1)
    return data


def main():
    user = check_password()

    if user:
        sns.set_theme()
        DATA = None

        page = st.sidebar.selectbox("Select a page", set_side_bar_options())

        if page == "Prediction Map":
            with st.sidebar:
                st.header("Weather Information")
                weather_info = weather_input()

            if isinstance(weather_info, pd.DataFrame):

                DATA, include_cols = combine_dataframes(weather_info)
                DATA = add_predictions(DATA, MODEL, include_cols, decision_boundary=0.9)
                DATA = GEOGRAPHY.merge(DATA, on="grid_id")
                DATA = DATA.merge(BUILDINGS_PCT, on="grid_id", how='left')
                DATA = calculate_risk(DATA)

                if isinstance(DATA, pd.DataFrame):
                    st.title("Storm Incidents Prediction")

                    amsterdam_map = create_amsterdam_map(
                        DATA[
                            ["geometry",
                             "count_building_year",
                             "count_vnl_locs",
                             "avg_building_year",
                             "predictions",
                             'grid_id',
                             'risk'
                             ]
                        ], SERVICE_AREAS
                    )
                    st.markdown(folium_static(amsterdam_map, width=1000, height=800), unsafe_allow_html=True)

        elif page == "Real Life Weather":
            get_data = GetWeatherDataModel().fetch_current_weather_data()
            if get_data.status == 'ok':
                weather_info = pd.DataFrame([get_data.get_initial_values()])
                DATA, include_cols = combine_dataframes(weather_info)
                DATA = add_predictions(DATA, MODEL, include_cols, decision_boundary=0.9)
                DATA = GEOGRAPHY.merge(DATA, on="grid_id")
                DATA = DATA.merge(BUILDINGS_PCT, on="grid_id", how='left')
                DATA = calculate_risk(DATA)
                st.title("Real Life Weather")
                if isinstance(DATA, pd.DataFrame):
                    st.title("")
                amsterdam_map = create_amsterdam_map(
                    DATA[
                        ["geometry",
                         "count_building_year",
                         "count_vnl_locs",
                         "avg_building_year",
                         "predictions",
                         'grid_id',
                         'risk'
                         ]
                    ], SERVICE_AREAS
                )
                st.markdown(folium_static(amsterdam_map, width=1000, height=800), unsafe_allow_html=True)

                # Display weather information on the left-hand side
                st.sidebar.subheader("Weather Information")
                st.sidebar.write(f"Temperature: {weather_info['temp'].values[0]:.2f}°C")
                st.sidebar.write(f"Humidity: {weather_info['humidity'].values[0]:.2f}%")
                st.sidebar.write(f"Wind Speed: {weather_info['wind_speed'].values[0]:.2f} m/s")
                st.sidebar.write(f"Wind Gust: {weather_info['wind_gust'].values[0]:.2f} m/s")
                st.sidebar.write(f"Rain in the last 1 hour: {weather_info['rain_1h'].values[0]} mm")
                st.sidebar.write(f"Snow in the last 1 hour: {weather_info['snow_1h'].values[0]} mm")




            else:
                st.write("Could Not connect to Open weather api. Please check your internet connection.")

        elif page == "XAI":
            explanation()


if __name__ == '__main__':
    main()