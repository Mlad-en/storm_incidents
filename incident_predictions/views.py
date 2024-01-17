from django.shortcuts import HttpResponse

from incident_predictions.models import (
    HighGroundWaterModel,
    TreesModel,
    AmsterdamGridModel,
    StormDamageModel,
    SoilModel,
    BuildingsModel,
    VunerableLocationsModel
)
from utils.high_ground_water import HighGroundWater, HighGroundWaterValidationModel
from utils.load_data import load_data_into_db
from utils.trees import TreesData, TreeColumnsEnglish, TreeValidationModel
from utils.predict_tree_age import generate_predictions
from utils.amsterdam_grid import AmsterdamGrid, GridValidationModel
from utils.storm_incidents import StormIncidents, StormDamageValidationModel
from utils.soil import SourceSoil, SoilValidationModel
from utils.buildings import SourceHistoricBuilding, BuildingsValidationModel
from utils.vunerable_locations import SourceVunerableLocations, LocationsValidationModel


import logging

logger = logging.getLogger(__name__)


def load_high_ground_water(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = HighGroundWater().clean_data().dataframe
        logger.info("Data Loaded")

        HighGroundWaterModel.objects.all().delete()
        load_data_into_db(data, HighGroundWaterValidationModel, HighGroundWaterModel, logger)
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
        TreesModel.objects.all().delete()
        load_data_into_db(data, TreeValidationModel, TreesModel, logger)
        return HttpResponse("Success")


def load_grid(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = AmsterdamGrid().clean_data().dataframe
        AmsterdamGridModel.objects.all().delete()
        load_data_into_db(data, GridValidationModel, AmsterdamGridModel, logger)
        return HttpResponse("Success")


def load_incidents(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = StormIncidents().clean_data().dataframe
        logger.info("Data Loaded")
        StormDamageModel.objects.all().delete()
        load_data_into_db(data, StormDamageValidationModel, StormDamageModel, logger)
        return HttpResponse("Success")


def load_soil(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceSoil().clean_data().dataframe
        logger.info("Data Loaded")

        SoilModel.objects.all().delete()
        load_data_into_db(data, SoilValidationModel, SoilModel, logger)
        return HttpResponse("Success")


def load_buildings(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceHistoricBuilding().clean_data().dataframe
        logger.info("Data Loaded")
        BuildingsModel.objects.all().delete()
        load_data_into_db(data, BuildingsValidationModel, BuildingsModel, logger)

        return HttpResponse("Success")


def load_vunerable_locations(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = SourceVunerableLocations().clean_data().dataframe
        logger.info("Data Loaded")
        VunerableLocationsModel.objects.all().delete()
        load_data_into_db(data, LocationsValidationModel, VunerableLocationsModel, logger)

        return HttpResponse("Success")

