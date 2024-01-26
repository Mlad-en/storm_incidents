import folium
import pandas as pd
import geopandas as gpd


def style_function(feature):
    grid_id = feature['properties']['id']
    risk_levels = {id_: 5 for id_ in grid_ids}
    risk_level = risk_levels.get(grid_id, 5)  # Default to risk level 5 (black) if not found
    colors = {1: 'green', 2: 'yellow', 3: 'orange', 4: 'red', 5: 'black'}

    return {
        'fillColor': colors[risk_level],  # Use risk level for fill color
        'color': colors[risk_level],  # Use risk level for border color
        'weight': 1,  # Set the border weight to 1
        'fillOpacity': 0.7,  # Set the fill opacity to 0.7
    }


def convert_model_to_geopandas(model_values):
    df = pd.DataFrame(list(model_values))
    wkt = df.geometry.apply(lambda x: x.wkt)
    df = gpd.GeoDataFrame(df, crs=4326, geometry=gpd.GeoSeries.from_wkt(wkt))
    return df


def convert_model_to_map(model_values):
    df = convert_model_to_geopandas(model_values)
    x1, y1, x2, y2 = df['geometry'].total_bounds
    amsterdam_map = folium.Map(tiles='openstreetmap')
    amsterdam_map.fit_bounds([[y1, x1], [y2, x2]])

    folium.GeoJson(
        df,
        style_function=lambda feature: {
            "fillColor": "#orange",
            "color": "blue",
            "opacity": 0.8,
            "weight": 0.1,
        },
        tooltip=folium.features.GeoJsonTooltip(fields=['grid_id'], labels=True, sticky=True)
    ).add_to(amsterdam_map)

    return amsterdam_map


def convert_predictions_to_map(predictions: pd.DataFrame):
    x1, y1, x2, y2 = predictions['geometry'].total_bounds
    amsterdam_map = folium.Map(tiles='openstreetmap')
    amsterdam_map.fit_bounds([[y1, x1], [y2, x2]])

    folium.GeoJson(
        predictions,
        style_function=lambda feature: {
            "fillColor": "#orange",
            "color": "blue",
            "opacity": 0.8,
            "weight": 0.1,
        },
        tooltip=folium.features.GeoJsonTooltip(fields=['grid_id', 'wind_speed', ''], labels=True, sticky=True)
    ).add_to(amsterdam_map)



    return amsterdam_map