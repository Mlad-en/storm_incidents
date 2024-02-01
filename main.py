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
from shapely import wkt
from folium import plugins

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

def create_risk_dataframe(trees, vn_buildings, building_pct_grid):
    # pre-processing vulnarable locs
    vuls = vn_buildings[['grid_id','count_vnl_locs']].set_index('grid_id')
    # pre-processing trees
    tree_data = pd.DataFrame()
    x = 0

    for column in trees.columns:
    
        if x >= 1 and x<= 7:
            if str(column)[-2:-1] == '_':
                number = int(str(column)[-1:])
            else:
                number = int(str(column)[-2:])
        
            tree_data[number] = trees[column] * number

        if x == 0:
            tree_data[column] = trees[column]

        x+=1
    mean_hight_grid = tree_data.set_index('grid_id').transpose().sum() / trees[["grid_id", "count_up_to_6","count_6_to_9", "count_9_to_12", "count_12_to_15", "count_15_to_18", "count_18_to_24", "count_over_24"]].set_index('grid_id').transpose().sum()
    trees_mean = pd.DataFrame(mean_hight_grid)
    newest = pd.DataFrame()
    newest['grid_id'] = mean_hight_grid.index
    newest['means'] = np.where(np.isnan(trees_mean), np.nanmean(trees_mean[0]), trees_mean)

    # Binning Functions
    def get_percentiles(distribution, percentages):
        threshold = dict()
        for x in percentages:
                threshold[x] = np.percentile(distribution, x)
        return threshold

    def define_bins(distribution, thresholds, column_name):
        binned = pd.DataFrame()
        for x in range(len(thresholds)):
            temp = pd.DataFrame()
            if x == 0:
                temp[column_name] = distribution[distribution <= thresholds[list(thresholds.keys())[x]]]
            else:
                temp[column_name] = distribution[(distribution <= thresholds[list(thresholds.keys())[x]]) & (distribution > thresholds[list(thresholds.keys())[x-1]])]
            temp[column_name] = np.where(temp[column_name] <= thresholds[list(thresholds.keys())[x]], x+1, temp[column_name])
            binned = pd.concat([binned, temp])
        return binned

    # Setting up final dataframe
    df1 = define_bins(building_pct_grid['sum_area_building'], get_percentiles(building_pct_grid['sum_area_building'], [20,40,60,80,100]), "building_percentages")
    df2 = define_bins(newest.set_index('grid_id')['means'], get_percentiles(newest.set_index('grid_id')['means'], [20,40,60,80,100]), "tree_height")
    df3 = define_bins(vuls['count_vnl_locs'], get_percentiles(vuls, [94.25,95,99.5,99.8,100]), "vulnarable_buildings")

    final = df1.merge(df3, left_index=True, right_index=True)
    final = final.merge(df2,left_index=True, right_index=True)

    return final


def create_amsterdam_map(amsterdam_gdf, service_areas):
    amsterdam_map = folium.Map(location=[52.3676, 4.9041], zoom_start=12)
    cast_types = ["count_building_year", "count_vnl_locs", "avg_building_year", "predictions"]
    amsterdam_gdf[cast_types] = amsterdam_gdf[cast_types].fillna(0).astype(int)

    def style_function(feature):
        prediction = feature["properties"]["predictions"]
        fill_opacity = 0.5 if prediction == 1 else 0  # Adjust the fillOpacity for red areas
        color = "red" if prediction == 1 else "none"
        return {"fillColor": color, "color": "black", "weight": 1, "fillOpacity": fill_opacity}

    child1 = folium.GeoJson(
        amsterdam_gdf,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['grid_id', 'avg_building_year', 'count_vnl_locs', 'predictions'], labels=True, sticky=True)
    )#.add_to(amsterdam_map)
    child1.layer_name = '100x100 grid'

    child2 = folium.GeoJson(service_areas["geometry"])#.add_to(amsterdam_map)
    child2.layer_name = 'Service Areas'
    amsterdam_map.add_children(child1)
    amsterdam_map.add_children(child2)
    # add the layer control
    folium.LayerControl().add_to(amsterdam_map)



    

    # Add additional points
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
        folium.Marker(location=[point[0], point[1]], popup=point[2], icon=folium.Icon(color='green')).add_to(amsterdam_map)

    return amsterdam_map


def weather_input():
    with st.form("Weather Information") as form:
        weather_main = st.selectbox(
            'What is the weather description?',
            ("Clear", "Thunderstorm", "Fog", "Smoke", "Snow", "Rain", "Mist", "Drizzle", "Clouds"))
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
SERVICE_AREAS = service_area_data_loading()
MODEL = load_model()

TREE_HEIGHT = load_tree_height()
GEOGRAPHY = full_geography()
BUILDINGS_PCT = load_building_pct()
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
    st.title("XAI")
    st.write("Add your content for Explanation here.")

def main():
    if check_password():
        sns.set_theme()
        DATA = None

        # Sidebar navigation
        page = st.sidebar.selectbox("Select a page", ["Prediction Map", "Real Life Weather", "XAI"])

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
                        ], SERVICE_AREAS
                    )
                    st.markdown(folium_static(amsterdam_map, width=1000, height=800), unsafe_allow_html=True)
        elif page == "Real Life Weather":
            real_life_weather()
        elif page == "Explanation":
            explanation()

if __name__ == '__main__':
    main()