class MapUrls:

    _open_data = "https://maps.amsterdam.nl/open_geodata"
    trees = f"{_open_data}/geojson_lnglat.php?KAARTLAAG=BOMEN&THEMA=bomen"
    high_groundwater = f"{_open_data}/geojson_lnglat.php?KAARTLAAG=RAINPROOF_DRAINAGE&THEMA=rainproof"
    soil = f"{_open_data}/geojson_lnglat.php?KAARTLAAG=BODEMKWALITEIT&THEMA=bodemkwaliteit"
    buildings = f"{_open_data}/geojson_lnglat.php?KAARTLAAG=BOUWJAAR&THEMA=bouwjaar"
