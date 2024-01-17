from pathlib import Path
from os.path import exists

import geopandas as gpd
from pydantic import BaseModel

from utils.geometry_types import PolygonField


class GridDutchColumns:
    ID = "id"
    GEOMETRY = "geometry"


class GridEnglishColumns:
    grid_id = "grid_id"
    geometry = "geometry"


class GridColumns:

    dutch = GridDutchColumns
    eng = GridEnglishColumns

    @classmethod
    def retain_columns(cls):
        return [cls.eng.grid_id, cls.eng.geometry]

    @classmethod
    def convert_column_names_to_eng(cls):
        return {
            cls.dutch.ID: cls.eng.grid_id,
            cls.dutch.GEOMETRY: cls.eng.geometry
        }


class AmsterdamGrid:
    def __init__(self):
        files_dir = Path(__file__).parents[1] / "files/amsterdam_grid.json"
        assert exists(files_dir)
        self.dataframe = gpd.read_file(files_dir)
        self.dataframe = self.dataframe.to_crs(epsg=4326)

    def clean_data(self):
        dataframe = self.dataframe.rename(columns=GridColumns.convert_column_names_to_eng())
        drop_cols = [col for col in dataframe if col not in GridColumns.retain_columns()]
        dataframe = dataframe.drop(drop_cols, axis=1)
        self.dataframe = dataframe
        return self


class GridValidationModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    grid_id: str
    geometry: PolygonField
