import numpy as np
import geopandas as gpd
from pydantic import BaseModel

from utils import resources
from utils.geometry_types import MultiPolygonField


class BuildingDutchColumns:
    BOUWJAAR = "Bouwjaar"
    GEOMETRY = "geometry"


class BuildingEnglishColumns:
    construction_year = "construction_year"
    geometry = "geometry"


class BuildingsColumns:

    dutch = BuildingDutchColumns
    eng = BuildingEnglishColumns

    @classmethod
    def convert_column_names_to_eng(cls):
        return {
            cls.dutch.BOUWJAAR: cls.eng.construction_year,
            cls.dutch.GEOMETRY: cls.eng.geometry,
        }

    @classmethod
    def get_column_types(cls):
        return {
            cls.eng.construction_year: np.uint16,
        }


class SourceHistoricBuilding:

    def __init__(self):
        self.dataframe = gpd.read_file(resources.MapUrls.buildings)

    def clean_data(self):
        dataframe = self.dataframe.rename(columns=BuildingsColumns.convert_column_names_to_eng())
        dataframe = dataframe.astype(BuildingsColumns.get_column_types())
        self.dataframe = dataframe
        return self


class BuildingsValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    construction_year: int
    geometry: MultiPolygonField
