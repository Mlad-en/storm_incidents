import overpy
import pandas as pd
import geopandas as gpd
from pydantic import BaseModel

from utils.geometry_types import GeometryField


class VunerableLocationDetails(BaseModel):

    name: str
    query_short_name: str
    area_name: str


class VunerableTypeDetails(BaseModel):
    name: str
    query: str | None = None

    @property
    def query_string(self):
        if not self.query:
            return self.name
        else:
            return self.query


class VunerableRegionName:
    UITHOORN = VunerableLocationDetails(name="Uithoorn", query_short_name="uith", area_name="uith")
    AALSMEER = VunerableLocationDetails(name="Aalsmeer", query_short_name="aalsmeer", area_name="aalsmeer")
    AMSTELVEEN = VunerableLocationDetails(name="Amstelveen", query_short_name="amstelveen", area_name="amstelveen")
    AMSTERDAM = VunerableLocationDetails(name="Amsterdam", query_short_name="amsterdam", area_name="amsterdam")
    DIEMEN = VunerableLocationDetails(name="Diemen", query_short_name="diemen", area_name="diemen")
    OUDER_AMSTEL = VunerableLocationDetails(name="Ouder-Amstel", query_short_name="ouder_amstel", area_name="ouder_amstel")


class VunerableBuildingTypes:
    KINDERGARTEN = VunerableTypeDetails(name="kindergarten")
    SCHOOL = VunerableTypeDetails(name="school")
    UNIVERSITY = VunerableTypeDetails(name="university")
    NURSING_HOME = VunerableTypeDetails(name="nursing_home", query='social_facility"]["social_facility"="nursing_home')


def get_coordinates_in_regions(query: str, region_name: str, building_type: VunerableTypeDetails):
    api = overpy.Overpass()
    coordinates = []

    result = api.query(query)

# Extract and store latitude, longitude, and region for each school within the region boundaries
    for node in result.nodes:
        building_name = node.tags.get("name", "N/A") # Get school name; if not available, use "N/A"
        school_coords = {
            'type': building_type.name,
            'region': region_name,
            'name': building_name,
            'latitude': node.lat,
            'longitude': node.lon
        }
        coordinates.append(school_coords)

    return coordinates


def generate_query(building_type: VunerableTypeDetails, building_details: VunerableLocationDetails):
    query = f"""area["name"="{building_details.name}"]->.{building_details.query_short_name};  
(  
node(area.{building_details.area_name})["amenity"="{building_type.query_string}"];  
way(area.{building_details.area_name})["amenity"="{building_type.query_string}"];  
relation(area.{building_details.area_name})["amenity"="{building_type.query_string}"];  
);  
out;  
"""

    return query


class SourceVunerableLocations:

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def clean_data(self):
        regions = [
            VunerableRegionName.UITHOORN,
            VunerableRegionName.AALSMEER,
            VunerableRegionName.AMSTELVEEN,
            VunerableRegionName.AMSTERDAM,
            VunerableRegionName.DIEMEN,
            VunerableRegionName.OUDER_AMSTEL
        ]

        types = [
            VunerableBuildingTypes.KINDERGARTEN,
            VunerableBuildingTypes.SCHOOL,
            VunerableBuildingTypes.UNIVERSITY,
            VunerableBuildingTypes.NURSING_HOME
        ]

        vunerable_list = []

        for type in types:
            for region in regions:
                query = generate_query(type, region)
                coords = get_coordinates_in_regions(query, region.name, type)
                vunerable_list.extend(coords)

        vunerable_df = pd.DataFrame(vunerable_list)
        vunerable_df = gpd.GeoDataFrame(
            vunerable_df,
            geometry=gpd.points_from_xy(vunerable_df.longitude, vunerable_df.latitude),
            crs=f'EPSG:{4326}'
        )
        vunerable_df = vunerable_df.drop(['latitude', 'longitude'], axis=1)
        self.dataframe = vunerable_df

        return self


class LocationsValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    type: str
    region: str
    name: str
    geometry: GeometryField

