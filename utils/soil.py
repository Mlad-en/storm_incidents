from typing import Annotated

import numpy as np
from django.contrib.gis.geos import MultiPolygon, GEOSGeometry
from pydantic import BeforeValidator, BaseModel
from shapely.wkt import dumps as shapely_dumps

from utils import resources
import geopandas as gpd

from utils.geometry_types import MultiPolygonField


class SoilDutchColumns:
    GEBIEDNUMMER = "Gebiednummer"
    LOCATIE = "Locatie"
    ZONE = "Zone"
    ZONE_WEG = "Zone_weg"
    BODEMFUNCTIE = "Bodemfunctie"
    LAAG_0_05 = "Laag_0_05"
    LAAG_05_1 = "Laag_05_1"
    LAAG_1_2 = "Laag_1_2"
    LAAG_2 = "Laag_2"
    TOELICHTING = "Toelichting"
    TOELICHTING_WEG = "Toelichting_weg"
    STATISTISCHE_KENGETALLEN = "Statistische_kengetallen"
    STATISTISCHE_KENGETALLEN_WEG = "Statistische_kengetallen_weg"
    GEOMETRY = "geometry"


class SoilEnglishColumns:
    area_number = "area_number"
    location = "location"
    zone = "zone"
    zone_road = "zone_road"
    soil_function = "soil_function"
    layer_0_05_meters = "layer_0_05_meters"
    layer_05_1_meters = "layer_05_1_meters"
    layer_1_2_meters = "layer_1_2_meters"
    layer_2_meters = "layer_2_meters"
    explanation = "explanation"
    explanation_road = "explanation_road"
    statistical_key_numbers = "statistical_key_numbers"
    statistical_key_numbers_road = "statistical_key_numbers_road"
    geometry = "geometry"


class SoilColumns:
    dutch = SoilDutchColumns
    eng = SoilEnglishColumns

    @classmethod
    def convert_column_names_to_eng(cls):
        return {
            cls.dutch.GEBIEDNUMMER: cls.eng.area_number,
            cls.dutch.LOCATIE: cls.eng.location,
            cls.dutch.ZONE: cls.eng.zone,
            cls.dutch.ZONE_WEG: cls.eng.zone_road,
            cls.dutch.BODEMFUNCTIE: cls.eng.soil_function,
            cls.dutch.LAAG_0_05: cls.eng.layer_0_05_meters,
            cls.dutch.LAAG_05_1: cls.eng.layer_05_1_meters,
            cls.dutch.LAAG_1_2: cls.eng.layer_1_2_meters,
            cls.dutch.LAAG_2: cls.eng.layer_2_meters,
            cls.dutch.TOELICHTING: cls.eng.explanation,
            cls.dutch.TOELICHTING_WEG: cls.eng.explanation_road,
            cls.dutch.STATISTISCHE_KENGETALLEN: cls.eng.statistical_key_numbers,
            cls.dutch.STATISTISCHE_KENGETALLEN_WEG: cls.eng.statistical_key_numbers_road
        }
    
    @classmethod
    def retain_columns(cls):
        return [cls.eng.location, cls.eng.zone, cls.eng.geometry, cls.eng.soil_function]

    @classmethod
    def get_column_types(cls):
        return {
            cls.eng.location: "category",
            cls.eng.zone: "category",
            cls.eng.soil_function: "category",
        }


class SourceSoil:

    def __init__(self):
        self.dataframe = gpd.read_file(resources.MapUrls.soil)

    def clean_data(self):
        dataframe = self.dataframe.rename(columns=SoilColumns.convert_column_names_to_eng())
        dataframe = dataframe.drop([
            col 
            for col 
            in dataframe.columns 
            if col not in SoilColumns.retain_columns()
            ], axis=1)
        dataframe = dataframe.astype(SoilColumns.get_column_types())
        self.dataframe = dataframe
        return self


class SoilValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    location: str
    zone: str
    soil_function: str
    geometry: MultiPolygonField
