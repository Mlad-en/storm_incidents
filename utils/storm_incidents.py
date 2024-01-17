import datetime
from os.path import exists
from pathlib import Path
from typing import Annotated

import numpy as np
import pandas as pd
import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry
from shapely.wkt import dumps as shapely_dumps
from pydantic import BeforeValidator, BaseModel
from shapely import Point


class StormDamageOriginalColumns:
    INCIDENT_ID = "Incident_ID"
    DATE = "Date"
    INCIDENT_STARTTIME = "Incident_Starttime"
    INCIDENT_ENDTIME = "Incident_Endtime"
    INCIDENT_DURATION = "Incident_Duration"
    DURATION_MINUTES = "Duration_Minutes"
    INCIDENT_PRIORITY = "Incident_Priority"
    SERVICE_AREA = "Service_Area"
    MUNICIPALITY = "Municipality"
    DAMAGE_TYPE = "Damage_Type"
    LONGITUDE = "LON"
    LATITUDE = "LAT"


class StormDamageEnglishColumns:
    incident_id = "incident_id"
    date = "date"
    incident_start_time = "incident_start_time"
    incident_end_time = "incident_end_time"
    incident_duration = "incident_duration"
    incident_priority = "incident_priority"
    service_area = "service_area"
    municipality = "municipality"
    damage_type = "damage_type"
    LONGITUDE = "LON"
    LATITUDE = "LAT"
    geometry = "geometry"

    @classmethod
    def get_column_types(cls):
        return {
            cls.incident_id: np.uint64,
            cls.incident_priority: np.float16,
            cls.service_area: "category",
            cls.municipality: "category",
            cls.damage_type: "category",
        }

    @classmethod
    def get_columns_conversions(cls):
        return {
            StormDamageOriginalColumns.INCIDENT_ID: cls.incident_id,
            StormDamageOriginalColumns.DATE: cls.date,
            StormDamageOriginalColumns.INCIDENT_STARTTIME: cls.incident_start_time,
            StormDamageOriginalColumns.INCIDENT_ENDTIME: cls.incident_end_time,
            StormDamageOriginalColumns.INCIDENT_DURATION: cls.incident_duration,
            StormDamageOriginalColumns.INCIDENT_PRIORITY: cls.incident_priority,
            StormDamageOriginalColumns.SERVICE_AREA: cls.service_area,
            StormDamageOriginalColumns.MUNICIPALITY: cls.municipality,
            StormDamageOriginalColumns.DAMAGE_TYPE: cls.damage_type,
            StormDamageOriginalColumns.LONGITUDE: cls.LONGITUDE,
            StormDamageOriginalColumns.LATITUDE: cls.LATITUDE,
        }


class StormIncidents:

    def __init__(self):
        files_dir = Path(__file__).parents[1] / "files/Stormdata & FireStations.xlsx"
        assert exists(files_dir)
        self.dataframe = pd.read_excel(
            files_dir, sheet_name="Storm Data"
        )

    def clean_data(self):

        dataframe = self.dataframe.rename(columns=StormDamageEnglishColumns.get_columns_conversions())
        dataframe[StormDamageEnglishColumns.incident_start_time] = pd.to_datetime(
            dataframe[StormDamageEnglishColumns.incident_start_time], format="%H:%M:%S"
        ).dt.time

        dataframe[StormDamageEnglishColumns.incident_end_time] = pd.to_datetime(
            dataframe[StormDamageEnglishColumns.incident_end_time], format="%H:%M:%S"
        ).dt.time

        dataframe[StormDamageEnglishColumns.incident_duration] = pd.to_datetime(
            dataframe[StormDamageEnglishColumns.incident_duration], format="%H:%M:%S"
        ).dt.time

        dataframe[StormDamageEnglishColumns.incident_priority] = (
            dataframe[StormDamageEnglishColumns.incident_priority]
            .fillna(-1)
        )

        points = dataframe.apply(
            lambda row: Point(
                row[StormDamageEnglishColumns.LONGITUDE],
                row[StormDamageEnglishColumns.LATITUDE],
            ),
            axis=1,
        )

        dataframe = gpd.GeoDataFrame(dataframe, geometry=points)
        dataframe.crs = "epsg:4326"

        dataframe = dataframe.drop(
            [StormDamageEnglishColumns.LONGITUDE, StormDamageEnglishColumns.LATITUDE],
            axis=1,
        )

        self.dataframe = dataframe
        return self


def convert_to_django_geometry(geom_obj):
    shapely_polygon = shapely_dumps(geom_obj)
    geometry = GEOSGeometry(shapely_polygon)
    return geometry


GeometryField = Annotated[GEOSGeometry, BeforeValidator(convert_to_django_geometry)]


class IncidentValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    incident_id: int
    date: datetime.date
    incident_start_time: datetime.time
    incident_end_time: datetime.time
    incident_duration: datetime.time
    incident_priority: int
    service_area: str
    municipality: str
    damage_type: str
    geometry: GeometryField
