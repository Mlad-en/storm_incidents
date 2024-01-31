from django.contrib.gis.db import models


class CountTreeDiameterView(models.Model):

    class Meta:
        db_table = "count_tree_diameter"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    count_01_02 = models.BigIntegerField()
    count_02_03 = models.BigIntegerField()
    count_03_05 = models.BigIntegerField()
    count_05_1 = models.BigIntegerField()
    count_1_15 = models.BigIntegerField()
    count_over_15 = models.BigIntegerField()
    count_unknown = models.BigIntegerField()


class CountTreeHeightView(models.Model):

    class Meta:
        db_table = "count_tree_height"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    count_up_to_6 = models.BigIntegerField()
    count_6_to_9 = models.BigIntegerField()
    count_9_to_12 = models.BigIntegerField()
    count_12_to_15 = models.BigIntegerField()
    count_15_to_18 = models.BigIntegerField()
    count_18_to_24 = models.BigIntegerField()
    count_over_24 = models.BigIntegerField()
    count_unknown = models.BigIntegerField()


class SoilPercentageOverlapView(models.Model):

    class Meta:
        db_table = "soil_pct_view"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    sum_area_1 = models.FloatField()
    sum_area_2 = models.FloatField()
    sum_area_3 = models.FloatField()
    sum_area_4 = models.FloatField()
    sum_area_5 = models.FloatField()
    sum_area_6 = models.FloatField()
    sum_area_7 = models.FloatField()
    sum_area_20 = models.FloatField()
    sum_area_remediation = models.FloatField()
    sum_area_unknown = models.FloatField()


class UnderWaterPercentageOverlapView(models.Model):

    class Meta:
        db_table = "underwater_pct_view"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    drainable = models.FloatField()
    not_drainable = models.FloatField()
    total_underwater = models.FloatField()


class TreeAgeDescription(models.Model):

    class Meta:
        db_table = "tree_age_description"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    tree_count = models.BigIntegerField()
    mean_tree_age = models.DecimalField(max_digits=30, decimal_places=26)
    std_tree_age = models.DecimalField(max_digits=30, decimal_places=26)
    min_age = models.BigIntegerField()
    max_age = models.BigIntegerField()
    percentile_25 = models.FloatField()
    percentile_75 = models.FloatField()


class CountTreeTypesView(models.Model):

    class Meta:
        db_table = "count_tree_types"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    count_type_not_free_growing = models.BigIntegerField()
    count_type_free_growing = models.BigIntegerField()
    count_type_fruit = models.BigIntegerField()
    count_type_candelabra = models.BigIntegerField()
    count_type_pollard = models.BigIntegerField()
    count_type_espalier = models.BigIntegerField()
    count_type_stump = models.BigIntegerField()
    count_type_topiary = models.BigIntegerField()
    count_type_missing = models.BigIntegerField()


class EnvironmentMetricsView(models.Model):

    class Meta:
        db_table = "environment_metrics"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    tree_count = models.BigIntegerField()
    mean_tree_age = models.BigIntegerField()
    std_tree_age = models.BigIntegerField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    percentile_25 = models.FloatField()
    percentile_75 = models.FloatField()
    count_acer = models.BigIntegerField()
    count_alnus = models.BigIntegerField()
    count_betula = models.BigIntegerField()
    count_carpinus = models.BigIntegerField()
    count_crataegus = models.BigIntegerField()
    count_fraxinus = models.BigIntegerField()
    count_malus = models.BigIntegerField()
    count_onbekend = models.BigIntegerField()
    count_overig = models.BigIntegerField()
    count_platanus = models.BigIntegerField()
    count_populus = models.BigIntegerField()
    count_prunus = models.BigIntegerField()
    count_quercus = models.BigIntegerField()
    count_robinia = models.BigIntegerField()
    count_salix = models.BigIntegerField()
    count_tilia = models.BigIntegerField()
    count_ulmus = models.BigIntegerField()
    count_01_02 = models.BigIntegerField()
    count_02_03 = models.BigIntegerField()
    count_03_05 = models.BigIntegerField()
    count_05_1 = models.BigIntegerField()
    count_1_15 = models.BigIntegerField()
    count_over_15 = models.BigIntegerField()
    count_unknown_diameter = models.BigIntegerField()
    count_up_to_6 = models.BigIntegerField()
    count_6_to_9 = models.BigIntegerField()
    count_9_to_12 = models.BigIntegerField()
    count_12_to_15 = models.BigIntegerField()
    count_15_to_18 = models.BigIntegerField()
    count_18_to_24 = models.BigIntegerField()
    count_over_24 = models.BigIntegerField()
    count_unknown_height = models.BigIntegerField()
    sum_area_1 = models.FloatField()
    sum_area_2 = models.FloatField()
    sum_area_3 = models.FloatField()
    sum_area_4 = models.FloatField()
    sum_area_5 = models.FloatField()
    sum_area_6 = models.FloatField()
    sum_area_7 = models.FloatField()
    sum_area_20 = models.FloatField()
    sum_area_remediation = models.FloatField()
    sum_area_unknown = models.FloatField()
    drainable = models.FloatField()
    not_drainable = models.FloatField()
    total_underwater = models.FloatField()


class EnvironmentMetricsGridWithIncidents(models.Model):

    class Meta:
        db_table = "grid_environment_with_incidents"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    tree_count = models.BigIntegerField()
    mean_tree_age = models.BigIntegerField()
    std_tree_age = models.BigIntegerField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    percentile_25 = models.FloatField()
    percentile_75 = models.FloatField()
    count_acer = models.BigIntegerField()
    count_alnus = models.BigIntegerField()
    count_betula = models.BigIntegerField()
    count_carpinus = models.BigIntegerField()
    count_crataegus = models.BigIntegerField()
    count_fraxinus = models.BigIntegerField()
    count_malus = models.BigIntegerField()
    count_onbekend = models.BigIntegerField()
    count_overig = models.BigIntegerField()
    count_platanus = models.BigIntegerField()
    count_populus = models.BigIntegerField()
    count_prunus = models.BigIntegerField()
    count_quercus = models.BigIntegerField()
    count_robinia = models.BigIntegerField()
    count_salix = models.BigIntegerField()
    count_tilia = models.BigIntegerField()
    count_ulmus = models.BigIntegerField()
    count_01_02 = models.BigIntegerField()
    count_02_03 = models.BigIntegerField()
    count_03_05 = models.BigIntegerField()
    count_05_1 = models.BigIntegerField()
    count_1_15 = models.BigIntegerField()
    count_over_15 = models.BigIntegerField()
    count_unknown_diameter = models.BigIntegerField()
    count_up_to_6 = models.BigIntegerField()
    count_6_to_9 = models.BigIntegerField()
    count_9_to_12 = models.BigIntegerField()
    count_12_to_15 = models.BigIntegerField()
    count_15_to_18 = models.BigIntegerField()
    count_18_to_24 = models.BigIntegerField()
    count_over_24 = models.BigIntegerField()
    count_unknown_height = models.BigIntegerField()
    sum_area_1 = models.FloatField()
    sum_area_2 = models.FloatField()
    sum_area_3 = models.FloatField()
    sum_area_4 = models.FloatField()
    sum_area_5 = models.FloatField()
    sum_area_6 = models.FloatField()
    sum_area_7 = models.FloatField()
    sum_area_20 = models.FloatField()
    sum_area_remediation = models.FloatField()
    sum_area_unknown = models.FloatField()
    drainable = models.FloatField()
    not_drainable = models.FloatField()
    total_underwater = models.FloatField()
    has_incident = models.BooleanField(default=False)


class GridBuildingsVunerableLocations(models.Model):

    class Meta:
        db_table = "grid_buildings_vn_locs"
        managed = False

    grid_id = models.CharField(max_length=255, primary_key=True)
    count_building_year = models.BigIntegerField()
    avg_building_year = models.IntegerField()
    count_vnl_locs = models.BigIntegerField()


class DailyWeatherView(models.Model):

    class Meta:
        db_table = "daily_weather"
        managed = False

    dt_iso = models.DateField()
    avg_temp = models.FloatField()
    avg_temp_min = models.FloatField()
    avg_temp_max = models.FloatField()
    avg_wind_deg = models.FloatField()
    avg_wind_gust = models.FloatField()
    avg_wind_speed = models.FloatField()
    avg_snow_1h = models.FloatField()
    avg_rain_1h = models.FloatField()
    weather_main_priority = models.IntegerField()
    weather_main = models.CharField(max_length=150)


class DailyWeatherWithIncidentsView(models.Model):

    class Meta:
        db_table = "daily_weather_with_incidents"
        managed = False

    dt_iso = models.DateField()
    avg_temp = models.FloatField()
    avg_temp_min = models.FloatField()
    avg_temp_max = models.FloatField()
    avg_wind_deg = models.FloatField()
    avg_wind_gust = models.FloatField()
    avg_wind_speed = models.FloatField()
    avg_snow_1h = models.FloatField()
    avg_rain_1h = models.FloatField()
    weather_main_priority = models.IntegerField()
    weather_main = models.CharField(max_length=150)
    count_incidents = models.BigIntegerField()
    has_incident = models.BooleanField()