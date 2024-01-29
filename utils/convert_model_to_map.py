import folium
import pandas as pd
import geopandas as gpd


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
    print(x1, y1, x2, y2)
    amsterdam_map = folium.Map(tiles='openstreetmap')
    amsterdam_map.fit_bounds([[y1, x1], [y2, x2]])
    predictions["grid_id"] = predictions["grid_id"].astype(str)
    cast_types = ["count", "count_vnl_locs", "avg_year", "predictions"]
    predictions[cast_types] = predictions[cast_types].fillna(0).astype(int)

    try:
        folium.GeoJson(
            predictions[["grid_id", "geometry"] + cast_types].fillna(0),
            style_function=lambda feature: {
                "fillColor": "#orange",
                "color": "blue",
                "opacity": 0.8,
                "weight": 0.1,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=cast_types,
                labels=True,
                sticky=True
            )
        ).add_to(amsterdam_map)

    except BaseException as e:
        print(e)

    return amsterdam_map._repr_html_()
