import geopandas as gpd
from pydantic import BaseModel

from utils import resources
from utils.geometry_types import MultiPolygonField


class HighWaterDutchColumns:
    LOCATIE = "Locatie"
    DRAINAGE = "Drainage"
    GEOMETRY = "geometry"


class HighWaterEnglishColumns:
    LOCATION = "location"
    DRAINAGE = "drainage"
    GEOMETRY = "geometry"


class DrainOptions:

    DRAIN_POSSIBLE_DUTCH = "Mogelijk"
    DRAIN_NOT_POSSIBLE_DUTCH = "Niet mogelijk"
    DRAIN_POSSIBLE_ENGLISH = "DRAIN_POSSIBLE"
    DRAIN_NOT_POSSIBLE_ENGLISH = "DRAIN_NOT_POSSIBLE"

    @classmethod
    def get_conversion(cls, item: str):
        conversions = {
            cls.DRAIN_POSSIBLE_DUTCH: cls.DRAIN_POSSIBLE_ENGLISH,
            cls.DRAIN_NOT_POSSIBLE_DUTCH: cls.DRAIN_NOT_POSSIBLE_ENGLISH
        }

        return conversions.get(item)


class HighGroundWaterColumns:

    eng = HighWaterEnglishColumns
    dutch = HighWaterDutchColumns

    @classmethod
    def convert_column_names_to_eng(cls):
        return {
            cls.dutch.LOCATIE: cls.eng.LOCATION,
            cls.dutch.DRAINAGE: cls.eng.DRAINAGE,
            cls.dutch.GEOMETRY: cls.eng.GEOMETRY
        }

    @classmethod
    def get_column_types(cls):
        return {
            cls.eng.LOCATION: "category",
            cls.eng.DRAINAGE: "category"
        }


class HighGroundWater:

    def __init__(self):
        self.dataframe = gpd.read_file(resources.MapUrls.high_groundwater)

    def clean_data(self):
        dataframe = self.dataframe.rename(columns=HighGroundWaterColumns.convert_column_names_to_eng())
        dataframe[HighWaterEnglishColumns.LOCATION] = dataframe[HighWaterEnglishColumns.LOCATION].fillna("Unknown")
        dataframe = dataframe.astype(HighGroundWaterColumns.get_column_types())

        dataframe[HighWaterEnglishColumns.DRAINAGE] = dataframe.apply(
            lambda x: DrainOptions.get_conversion(x[HighWaterEnglishColumns.DRAINAGE]),
            axis=1
        )
        self.dataframe = dataframe

        return self


class HighGroundWaterValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    location: str
    drainage: str
    geometry: MultiPolygonField
