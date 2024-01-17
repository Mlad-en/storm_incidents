from pathlib import Path

import pandas as pd
from django.db import transaction
from django.shortcuts import HttpResponse

from incident_predictions.models import HighGroundWaterModel, TreesModel, AmsterdamGridModel, StormDamageModel
from utils.high_ground_water import HighGroundWater, HighGroundWaterValidationModel
from utils.trees import TreesData, TreeColumnsEnglish, TreeValidationModel
from utils.predict_tree_age import generate_predictions
from utils.amsterdam_grid import AmsterdamGrid, GridValidationModel
from utils.storm_incidents import StormIncidents, IncidentValidationModel


import logging

logger = logging.getLogger(__name__)


def load_high_ground_water(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = HighGroundWater().clean_data().dataframe
        logger.info("Data Loaded")

        HighGroundWaterModel.objects.all().delete()

        for record in data.to_dict("records"):
            high_groundwater_record = HighGroundWaterValidationModel(**record)

            HighGroundWaterModel.objects.update_or_create(**high_groundwater_record.model_dump())

            logger.info("Record loaded successfully.")

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
        with transaction.atomic():
            for record in data.to_dict("records"):
                tree_record = TreeValidationModel(**record)
                TreesModel.objects.create(**tree_record.model_dump())

                logger.info("Record loaded successfully.")

        return HttpResponse("Success")


def load_grid(request):
    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = AmsterdamGrid().clean_data().dataframe

        AmsterdamGridModel.objects.all().delete()
        with transaction.atomic():
            for record in data.to_dict("records"):
                grid_record = GridValidationModel(**record)
                AmsterdamGridModel.objects.update_or_create(**grid_record.model_dump())

                logger.info("Record loaded successfully.")

        return HttpResponse("Success")


def load_incidents(request):

    if request.method == 'GET':  # TODO: Update either method or shift into the admin page
        logger.info("Method Started")
        data = StormIncidents().clean_data().dataframe
        logger.info("Data Loaded")

        StormDamageModel.objects.all().delete()

        with transaction.atomic():
            for record in data.to_dict("records"):
                incident_record = IncidentValidationModel(**record)
                StormDamageModel.objects.create(**incident_record.model_dump())
                logger.info("Record loaded successfully.")
        return HttpResponse("Success")
