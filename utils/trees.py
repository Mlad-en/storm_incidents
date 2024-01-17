from typing import Annotated

import numpy as np
import geopandas as gpd
import pandas as pd
from pydantic import BeforeValidator, BaseModel
from shapely.wkt import dumps as shapely_dumps
from django.contrib.gis.geos import GEOSGeometry


from utils import resources


class TreeColumnsDutch:
    ID = 'id'
    SOORTNAAM = 'soortnaam'
    SOORTNAAMKORT = 'soortnaamKort'
    SOORTNAAMNL = 'SoortnaamNL'
    SOORTNAAMTOP = 'soortnaamTop'
    BOOMHOOGTEKLASSEACTUEEL = 'boomhoogteklasseActueel'
    STAMDIAMETERKLASSE = 'stamdiameterklasse'
    JAARVANAANLEG = 'jaarVanAanleg'
    TYPEOBJECT = 'typeObject'
    STANDPLAATSGEDETAILLEERD = 'standplaatsGedetailleerd'
    TYPEBEHEERDERPLUS = 'typeBeheerderPlus'
    TYPEEIGENAARPLUS = 'typeEigenaarPlus'
    GEOMETRY = 'geometry'


class TreeColumnsEnglish:
    tree_id = 'tree_id'
    species_name = 'species_name'
    species_name_short = 'species_name_short'
    species_name_nl = 'species_name_nl'
    species_name_top = 'species_name_top'
    tree_height = 'tree_height'
    trunk_diameter_class = 'trunk_diameter_class'
    plant_year = 'plant_year'
    tree_age = 'tree_age'
    predicted_age = 'predicted_age'
    tree_type = 'tree_type'
    location_detailed = 'location_detailed'
    type_manager = 'type_manager'
    type_owner = 'type_owner'
    geometry = 'geometry'


class TReeHeightOptions:

    HEIGHT_UNKNOWN_ORIGINAL = "HEIGHT_UNKNOWN"
    HEIGHT_UP_TO_6M_ORIGINAL = "a. tot 6 m."
    HEIGHT_6_TO_9M_ORIGINAL = "b. 6 tot 9 m."
    HEIGHT_9_TO_12M_ORIGINAL = "c. 9 tot 12 m."
    HEIGHT_12_TO_15M_ORIGINAL = "d. 12 tot 15 m."
    HEIGHT_15_TO_18M_ORIGINAL = "e. 15 tot 18 m."
    HEIGHT_18_TO_24M_ORIGINAL = "f. 18 tot 24 m."
    HEIGHT_OVER_24M_ORIGINAL = "g. 24 m. en hoger"

    HEIGHT_UNKNOWN = "HEIGHT_UNKNOWN"
    HEIGHT_UP_TO_6M = "HEIGHT_UP_TO_6M"
    HEIGHT_6_TO_9M = "HEIGHT_6_TO_9M"
    HEIGHT_9_TO_12M = "HEIGHT_9_TO_12M"
    HEIGHT_12_TO_15M = "HEIGHT_12_TO_15M"
    HEIGHT_15_TO_18M = "HEIGHT_15_TO_18M"
    HEIGHT_18_TO_24M = "HEIGHT_18_TO_24M"
    HEIGHT_OVER_24M = "HEIGHT_OVER_24M"

    @classmethod
    def get_conversion(cls, item: str):
        conversions = {
            cls.HEIGHT_UNKNOWN_ORIGINAL: cls.HEIGHT_UNKNOWN,
            cls.HEIGHT_UP_TO_6M_ORIGINAL: cls.HEIGHT_UP_TO_6M,
            cls.HEIGHT_6_TO_9M_ORIGINAL: cls.HEIGHT_6_TO_9M,
            cls.HEIGHT_9_TO_12M_ORIGINAL: cls.HEIGHT_9_TO_12M,
            cls.HEIGHT_12_TO_15M_ORIGINAL: cls.HEIGHT_12_TO_15M,
            cls.HEIGHT_15_TO_18M_ORIGINAL: cls.HEIGHT_15_TO_18M,
            cls.HEIGHT_18_TO_24M_ORIGINAL: cls.HEIGHT_18_TO_24M,
            cls.HEIGHT_OVER_24M_ORIGINAL: cls.HEIGHT_OVER_24M
        }

        return conversions.get(item, cls.HEIGHT_UNKNOWN)

    @classmethod
    def get_categories_order(cls):
        return pd.CategoricalDtype(
            categories=[
                cls.HEIGHT_UNKNOWN,
                cls.HEIGHT_UP_TO_6M,
                cls.HEIGHT_6_TO_9M,
                cls.HEIGHT_9_TO_12M,
                cls.HEIGHT_12_TO_15M,
                cls.HEIGHT_15_TO_18M,
                cls.HEIGHT_18_TO_24M,
                cls.HEIGHT_OVER_24M
            ],
            ordered=True
        )


class TrunkDiameterOptions:

    FROM_0_1_TO_0_2_ORIGINAL = '0,1 tot 0,2 m.'
    FROM_0_2_TO_0_3_ORIGINAL = '0,2 tot 0,3 m.'
    FROM_0_3_TO_0_5_ORIGINAL = '0,3 tot 0,5 m.'
    FROM_0_5_TO_1_ORIGINAL = '0,5 tot 1 m.'
    FROM_1_TO_1_5_ORIGINAL = '1,0 tot 1,5 m.'
    OVER_1_5_ORIGINAL = '1,5 m. en grot'
    UNKNOWN_ORIGINAL = 'Onbekend'

    FROM_0_1_TO_0_2 = 'FROM_0_1_TO_0_2_M'
    FROM_0_2_TO_0_3 = 'FROM_0_2_TO_0_3_M'
    FROM_0_3_TO_0_5 = 'FROM_0_3_TO_0_5_M'
    FROM_0_5_TO_1 = 'FROM_0_5_TO_1_M'
    FROM_1_TO_1_5 = 'FROM_1_TO_1_5_M'
    OVER_1_5 = 'OVER_1_5_M'
    DIAMETER_UNKNOWN = 'UNKNOWN'

    @classmethod
    def get_conversion(cls, item: str):
        conversions = {
            cls.FROM_0_1_TO_0_2_ORIGINAL: cls.FROM_0_1_TO_0_2,
            cls.FROM_0_2_TO_0_3_ORIGINAL: cls.FROM_0_2_TO_0_3,
            cls.FROM_0_3_TO_0_5_ORIGINAL: cls.FROM_0_3_TO_0_5,
            cls.FROM_0_5_TO_1_ORIGINAL: cls.FROM_0_5_TO_1,
            cls.FROM_1_TO_1_5_ORIGINAL: cls.FROM_1_TO_1_5,
            cls.OVER_1_5_ORIGINAL: cls.OVER_1_5,
            cls.UNKNOWN_ORIGINAL: cls.DIAMETER_UNKNOWN,
        }

        return conversions.get(item, cls.DIAMETER_UNKNOWN)

    @classmethod
    def get_conversions(cls):
        return {
            cls.FROM_0_1_TO_0_2_ORIGINAL: cls.FROM_0_1_TO_0_2,
            cls.FROM_0_2_TO_0_3_ORIGINAL: cls.FROM_0_2_TO_0_3,
            cls.FROM_0_3_TO_0_5_ORIGINAL: cls.FROM_0_3_TO_0_5,
            cls.FROM_0_5_TO_1_ORIGINAL: cls.FROM_0_5_TO_1,
            cls.FROM_1_TO_1_5_ORIGINAL: cls.FROM_1_TO_1_5,
            cls.OVER_1_5_ORIGINAL: cls.OVER_1_5,
            cls.UNKNOWN_ORIGINAL: cls.DIAMETER_UNKNOWN,
        }

    @classmethod
    def get_categories_order(cls):
        return pd.CategoricalDtype(
            categories=[
                cls.DIAMETER_UNKNOWN,
                cls.FROM_0_1_TO_0_2,
                cls.FROM_0_2_TO_0_3,
                cls.FROM_0_3_TO_0_5,
                cls.FROM_0_5_TO_1,
                cls.FROM_1_TO_1_5,
                cls.OVER_1_5,
            ],
            ordered=True
        )


class TreeColumns:
    eng = TreeColumnsEnglish
    dutch = TreeColumnsDutch

    @classmethod
    def convert_column_names_to_eng(cls):
        return {
            cls.dutch.ID: cls.eng.tree_id,
            cls.dutch.SOORTNAAM: cls.eng.species_name,
            cls.dutch.SOORTNAAMKORT: cls.eng.species_name_short,
            cls.dutch.SOORTNAAMNL: cls.eng.species_name_nl,
            cls.dutch.SOORTNAAMTOP: cls.eng.species_name_top,
            cls.dutch.BOOMHOOGTEKLASSEACTUEEL: cls.eng.tree_height,
            cls.dutch.STAMDIAMETERKLASSE: cls.eng.trunk_diameter_class,
            cls.dutch.JAARVANAANLEG: cls.eng.plant_year,
            cls.dutch.TYPEOBJECT: cls.eng.tree_type,
            cls.dutch.STANDPLAATSGEDETAILLEERD: cls.eng.location_detailed,
            cls.dutch.TYPEBEHEERDERPLUS: cls.eng.type_manager,
            cls.dutch.TYPEEIGENAARPLUS: cls.eng.type_owner,
            cls.dutch.GEOMETRY: cls.eng.geometry,
        }

    @classmethod
    def get_column_types(cls):
        return {
            cls.eng.tree_id: np.uint64,
            cls.eng.species_name_nl: "category",
            cls.eng.species_name_top: "category",
            cls.eng.species_name_short: "category",
            cls.eng.species_name: "category",
            cls.eng.location_detailed: "category",
            cls.eng.tree_height: TReeHeightOptions.get_categories_order(),
            cls.eng.trunk_diameter_class: TrunkDiameterOptions.get_categories_order(),
            cls.eng.tree_type: "category",
            cls.eng.plant_year: np.uint16,
            cls.eng.tree_age: np.uint16,
        }


class TreesData:
    def __init__(self):
        self.dataframe = gpd.read_file(resources.MapUrls.trees)

    def clean_data(self):
        dataframe = self.dataframe.rename(columns=TreeColumns.convert_column_names_to_eng())

        dataframe[TreeColumnsEnglish.tree_height] = (
            dataframe[TreeColumnsEnglish.tree_height]
            .apply(lambda x: TReeHeightOptions.get_conversion(x))
        )

        dataframe[TreeColumnsEnglish.trunk_diameter_class] = (
            dataframe[TreeColumnsEnglish.trunk_diameter_class]
            .apply(lambda x: TrunkDiameterOptions.get_conversion(x))
        )

        dataframe[TreeColumnsEnglish.tree_age] = dataframe.apply(
            lambda row:
                2024 - row[TreeColumnsEnglish.plant_year]
                if row[TreeColumnsEnglish.plant_year] > 1800
                else 0,
            axis=1
        )

        dataframe = dataframe.astype(TreeColumns.get_column_types())

        self.dataframe = dataframe

        return self


def convert_to_django_geometry(geom_obj):
    shapely_polygon = shapely_dumps(geom_obj)
    geometry = GEOSGeometry(shapely_polygon)
    return geometry


GeometryField = Annotated[GEOSGeometry, BeforeValidator(convert_to_django_geometry)]


class TreeValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    tree_id: int
    species_name: str
    species_name_short: str
    species_name_nl: str
    species_name_top: str
    tree_height: str
    trunk_diameter_class: str
    plant_year: int
    tree_age: int
    predicted_age: bool
    tree_type: str
    location_detailed: str
    type_manager: str
    type_owner: str
    geometry: GeometryField
