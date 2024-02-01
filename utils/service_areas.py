from os.path import exists
from pathlib import Path

import pandas as pd
import geopandas as gpd
from pydantic import BaseModel
from shapely import wkt

from utils.geometry_types import MultiPolygonField


class ServiceAreasOriginalColumns:
    verzorgingsgebied_ID = "H_Verzorgingsgebied_ID"
    verzorgingsgebied_name = "Verzorgingsgebied"
    geom = "geom"
    geomtext = "geomtext"

class ServiceAreasEnglishColumns:
    service_area_id = "service_area_id"
    service_area_name = "service_area_name"
    geom = "geom"
    geometry = "geometry"

    @classmethod
    def get_column_types(cls):
        return {
            cls.service_area_id: "category",
            cls.service_area_name: "category",
        }

    @classmethod
    def get_columns_conversions(cls):
        return {
            ServiceAreasOriginalColumns.verzorgingsgebied_ID: cls.service_area_id,
            ServiceAreasOriginalColumns.verzorgingsgebied_name: cls.service_area_name,
            ServiceAreasOriginalColumns.geom: cls.geom,
            ServiceAreasOriginalColumns.geomtext: cls.geometry,
        }

class ServiceAreas:

    def __init__(self):
        files_dir = Path(__file__).resolve().parents[1] / "files/Verzorgingsgebieden_VrAA.csv"
        assert exists(files_dir)
        self.dataframe = pd.read_csv(
            files_dir
        )

    def clean_data(self):
        dataframe = self.dataframe.rename(columns=ServiceAreasEnglishColumns.get_columns_conversions())
        dataframe['geometry'] = dataframe['geometry'].apply(wkt.loads)
        dataframe = gpd.GeoDataFrame(dataframe, crs='epsg:4326')
        dataframe = dataframe.drop(['geom'], axis=1)
        self.dataframe = dataframe
        return self


class ServiceAreasModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    service_area_id: int
    service_area_name: str
    geometry: MultiPolygonField
