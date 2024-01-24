import folium
from django.shortcuts import HttpResponse, render

from incident_predictions import models
from incident_predictions import forms
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


def weather_predictions(request):
    context = {}

    m = folium.Map([51.5, -0.25], zoom_start=10)
    test = folium.Html('<b>Hello world</b>', script=True)
    popup = folium.Popup(test, max_width=2650)
    folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
    m= m._repr_html_()
    context = {'my_map': m}

    if request.method == 'GET':
        context['form'] = forms.WeatherDataForm()
        return render(request, "incident_predictions/weather_predictions.html", context)

    if request.method == 'POST':
        form = forms.WeatherDataForm(request.POST or None)
        context['form'] = form
        print(form.is_valid())
        if form.is_valid():
            return HttpResponse("Success")

        else:
            return render(request, "incident_predictions/weather_predictions.html", context, status=400)
