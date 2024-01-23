from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse
import folium
#from shapely.geometry import Polygon, MultiPolygon
#from shapely.geometry import Point
#import psycopg2
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
#import io
#import joblib
import geopandas as gpd
#import ssl

from django.shortcuts import HttpResponse

from incident_predictions import models
from utils.high_ground_water import HighGroundWater, HighGroundWaterValidationModel
from utils.load_data import load_data_into_db
from utils.trees import TreesData, TreeColumnsEnglish, TreeValidationModel
from utils.predict_tree_age import generate_predictions
from utils.amsterdam_grid import AmsterdamGrid, GridValidationModel
from utils.storm_incidents import StormIncidents, StormDamageValidationModel
from utils.soil import SourceSoil, SoilValidationModel
from utils.buildings import SourceHistoricBuilding, BuildingsValidationModel
from utils.vunerable_locations import SourceVunerableLocations, LocationsValidationModel
from utils.weather_data import SourceWeatherData, WeatherDataValidationModel


import logging

logger = logging.getLogger(__name__)


def load_high_ground_water(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = HighGroundWater().clean_data().dataframe
        logger.info("Data Loaded")

        models.HighGroundWaterModel.objects.all().delete()
        load_data_into_db(data, HighGroundWaterValidationModel, models.HighGroundWaterModel, logger)
        return HttpResponse("Success")


def load_tree_data(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        data = TreesData().clean_data().dataframe
        logger.info("Data Loaded")
        data[TreeColumnsEnglish.predicted_age] = False

        logger.info("Predicting Data")
        data = generate_predictions(data)
        logger.info("Predicting Finished")
        logger.info("Beginning Data Load")
        models.TreesModel.objects.all().delete()
        load_data_into_db(data, TreeValidationModel, models.TreesModel, logger)
        return HttpResponse("Success")


def load_grid(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = AmsterdamGrid().clean_data().dataframe
        models.AmsterdamGridModel.objects.all().delete()
        load_data_into_db(data, GridValidationModel, models.AmsterdamGridModel, logger)
        return HttpResponse("Success")


def load_incidents(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = StormIncidents().clean_data().dataframe
        logger.info("Data Loaded")
        models.StormDamageModel.objects.all().delete()
        load_data_into_db(data, StormDamageValidationModel, models.StormDamageModel, logger)
        return HttpResponse("Success")


def load_soil(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceSoil().clean_data().dataframe
        logger.info("Data Loaded")

        models.SoilModel.objects.all().delete()
        load_data_into_db(data, SoilValidationModel, models.SoilModel, logger)
        return HttpResponse("Success")


def load_buildings(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceHistoricBuilding().clean_data().dataframe
        logger.info("Data Loaded")
        models.BuildingsModel.objects.all().delete()
        load_data_into_db(data, BuildingsValidationModel, models.BuildingsModel, logger)

        return HttpResponse("Success")


def load_vunerable_locations(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceVunerableLocations().clean_data().dataframe
        logger.info("Data Loaded")
        models.VunerableLocationsModel.objects.all().delete()
        load_data_into_db(data, LocationsValidationModel, models.VunerableLocationsModel, logger)

        return HttpResponse("Success")


def load_weather_data(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceWeatherData().clean_data().dataframe
        logger.info("Data Loaded")
        models.WeatherDataModel.objects.all().delete()
        load_data_into_db(data, WeatherDataValidationModel, models.WeatherDataModel, logger)

        return HttpResponse("Success")

def home(request):

  
 
  df = pd.DataFrame(list(models.AmsterdamGridModel.objects.all().values()))
  
  
  wkt = df.geometry.apply(lambda x: x.wkt)
  df = gpd.GeoDataFrame(df, crs=4326, geometry=gpd.GeoSeries.from_wkt(wkt))
  x1,y1,x2,y2 = df['geometry'].total_bounds
  
  amsterdam_map = folium.Map(tiles='openstreetmap')
  amsterdam_map.fit_bounds([[y1, x1], [y2, x2]])
  folium.GeoJson(df["geometry"], style_function=lambda feature: {
        "fillColor": "#orange",
        "color": "blue",
        "opacity": 0.8,
        "weight": 0.1,
    },).add_to(amsterdam_map)

# Render the map in the Django template
 # Render the map in the Django template
  return render(request, 'myfirst.html', {'amsterdam_map': amsterdam_map._repr_html_()})

