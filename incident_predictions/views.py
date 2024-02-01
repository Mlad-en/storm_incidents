import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponse, render, redirect

from incident_predictions import models, forms, database_views
from utils.convert_model_to_map import convert_model_to_map, convert_model_to_geopandas, convert_predictions_to_map
from utils.high_ground_water import HighGroundWater, HighGroundWaterValidationModel
from utils.load_data import load_data_into_db
from utils.predictive_model_utils import get_model_choices, load_model
from utils.trees import TreesData, TreeColumnsEnglish, TreeValidationModel
from utils.predict_tree_age import generate_predictions
from utils.amsterdam_grid import AmsterdamGrid, GridValidationModel
from utils.storm_incidents import StormIncidents, StormDamageValidationModel
from utils.soil import SourceSoil, SoilValidationModel
from utils.buildings import SourceHistoricBuilding, BuildingsValidationModel
from utils.vunerable_locations import SourceVunerableLocations, LocationsValidationModel
from utils.weather_api_model import GetWeatherDataModel
from utils.weather_data import SourceWeatherData, WeatherDataValidationModel
from utils.service_areas import ServiceAreasModel, ServiceAreas2
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


def load_service_area_data(request):

    if request.method == 'GET':
        logger.info("Method Started")
        data = ServiceAreas2().clean_data().dataframe
        logger.info("Data Loaded")
        models.ServiceAreasDataModel.objects.all().delete()
        load_data_into_db(data, ServiceAreasModel, models.ServiceAreasDataModel, logger)

        return HttpResponse('Success')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(None, data=request.POST)
        print(f"Form Data: {form.is_valid()}")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(f"Form User: {user}")
            if user is not None:
                login(request, user)
                print(request, f'Welcome, {username}!')
                return redirect('/weather_current')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'incident_predictions/login.html', {'form': form})


def weather_predictions(request):

    context = {}
    amsterdam_grid = models.AmsterdamGridModel.objects.all().values()
    amsterdam_map = convert_model_to_map(amsterdam_grid)
    context["amsterdam_map"] = amsterdam_map._repr_html_()

    predictive_models = models.PredictiveModels.objects.all()
    choices = get_model_choices(predictive_models)

    if request.method == 'GET':
        form = forms.WeatherDataForm(request.POST)
        form.fields["model"].choices = choices
        context['form'] = form
        return render(request, "incident_predictions/base.html", context)

    if request.method == 'POST':
        form = forms.WeatherDataForm(request.POST)
        form.fields["model"].choices = choices
        context['form'] = form

        if form.is_valid():
            amsterdam_geo = convert_model_to_geopandas(amsterdam_grid)
            grid_info = database_views.EnvironmentMetricsGridWithIncidents.objects.all().values()
            grid_info = pd.DataFrame(list(grid_info))
            buildings_locations = database_views.GridBuildingsVunerableLocations.objects.all().values()
            buildings_locations = pd.DataFrame(list(buildings_locations))

            weather_df = form.convert_to_dataframe()
            weather_df = weather_df.merge(grid_info, how="cross")
            predictive_model, model_type = load_model(form.cleaned_data, predictive_models)
            predictions = predictive_model.predict(weather_df)
            weather_df = weather_df.merge(grid_info, on="grid_id")
            weather_df = weather_df.assign(predictions=predictions).copy()
            weather_df = amsterdam_geo.merge(weather_df, on="grid_id")
            weather_df = weather_df.merge(buildings_locations, on="grid_id", how="left")
            amsterdam_map = convert_predictions_to_map(weather_df)
            context["amsterdam_map"] = amsterdam_map

            return render(request, "incident_predictions/base.html", context, status=200)

        else:
            return render(request, "incident_predictions/base.html", context, status=400)


def weather_current(request):

    if request.method == 'GET':
        context = {}
        data = GetWeatherDataModel().fetch_current_weather_data()
        if not data.status == "ok":
            return HttpResponse(data.status, status=400)

        form = forms.WeatherDataForm(initial=data.get_initial_values())
        context['form'] = form
        amsterdam_map = convert_model_to_map(models.AmsterdamGridModel.objects.all().values())
        context["amsterdam_map"] = amsterdam_map._repr_html_()

        return render(request, "incident_predictions/weather_current.html", context, status=200)
