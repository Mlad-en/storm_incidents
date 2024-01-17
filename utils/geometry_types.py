from typing import Annotated


from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
from pydantic import BeforeValidator
from shapely.wkt import dumps as shapely_dumps


def convert_to_django_geometry(geom_obj):
    shapely_polygon = shapely_dumps(geom_obj)
    geometry = GEOSGeometry(shapely_polygon)
    return geometry


def convert_to_django_multipolygon(geom_obj):
    shapely_polygon = shapely_dumps(geom_obj)
    geometry = GEOSGeometry(shapely_polygon)
    if geometry.geom_type != 'MultiPolygon':
        geometry = MultiPolygon([geometry])
    return geometry


GeometryField = Annotated[GEOSGeometry, BeforeValidator(convert_to_django_geometry)]

PolygonField = Annotated[Polygon, BeforeValidator(convert_to_django_geometry)]

MultiPolygonField = Annotated[MultiPolygon, BeforeValidator(convert_to_django_multipolygon)]
