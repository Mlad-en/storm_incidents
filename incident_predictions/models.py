from django.contrib.gis.db import models


class HighGroundWaterModel(models.Model):

    class Meta:
        db_table = "incident_predictions_high_groundwater"
        verbose_name = "high ground water"
        verbose_name_plural = "high ground water"

    DRAINAGE_CHOICES = [
        ('DRAIN_POSSIBLE', 'DRAIN_POSSIBLE'),
        ('DRAIN_NOT_POSSIBLE', 'DRAIN_NOT_POSSIBLE'),
    ]

    location = models.CharField(max_length=200)
    drainage = models.CharField(max_length=20, choices=DRAINAGE_CHOICES)
    geometry = models.MultiPolygonField()


class TreesModel(models.Model):

    class Meta:
        db_table = "incident_predictions_trees"
        verbose_name = "tree"
        verbose_name_plural = "trees"

    TREE_HEIGHT_CHOICES = [
        ('HEIGHT_UNKNOWN', 'HEIGHT_UNKNOWN'),
        ('HEIGHT_UP_TO_6M', 'HEIGHT_UP_TO_6M'),
        ('HEIGHT_6_TO_9M', 'HEIGHT_6_TO_9M'),
        ('HEIGHT_9_TO_12M', 'HEIGHT_9_TO_12M'),
        ('HEIGHT_12_TO_15M', 'HEIGHT_12_TO_15M'),
        ('HEIGHT_15_TO_18M', 'HEIGHT_15_TO_18M'),
        ('HEIGHT_18_TO_24M', 'HEIGHT_18_TO_24M'),
        ('HEIGHT_OVER_24M', 'HEIGHT_OVER_24M'),
    ]

    TREE_DIAMETER_CHOICES = [
        ('FROM_0_1_TO_0_2_M', 'FROM_0_1_TO_0_2_M'),
        ('FROM_0_2_TO_0_3_M', 'FROM_0_2_TO_0_3_M'),
        ('FROM_0_3_TO_0_5_M', 'FROM_0_3_TO_0_5_M'),
        ('FROM_0_5_TO_1_M', 'FROM_0_5_TO_1_M'),
        ('FROM_1_TO_1_5_M', 'FROM_1_TO_1_5_M'),
        ('OVER_1_5_M', 'OVER_1_5_M'),
        ('UNKNOWN', 'UNKNOWN'),
    ]

    tree_id = models.IntegerField()
    species_name = models.CharField(max_length=255)
    species_name_short = models.CharField(max_length=255, null=False)
    species_name_nl = models.CharField(max_length=255)
    species_name_top = models.CharField(max_length=255, null=False)
    tree_height = models.CharField(max_length=100, choices=TREE_HEIGHT_CHOICES, null=False)
    trunk_diameter_class = models.CharField(max_length=100, choices=TREE_DIAMETER_CHOICES, null=False)
    plant_year = models.IntegerField()
    tree_age = models.IntegerField(null=False)
    predicted_age = models.BooleanField(null=False, default=False)
    tree_type = models.CharField(max_length=255, null=False)
    location_detailed = models.CharField(max_length=255)
    type_manager = models.CharField(max_length=255)
    type_owner = models.CharField(max_length=255)
    geometry = models.PointField()


class AmsterdamGridModel(models.Model):

    class Meta:
        db_table = "incident_predictions_amsterdam_grid"
        verbose_name = "amsterdam grid"
        verbose_name_plural = "amsterdam grids"

    grid_id = models.CharField(max_length=255, null=False)
    geometry = models.PolygonField()


class StormDamageModel(models.Model):

    class Meta:
        db_table = "incident_predictions_storm_damage"
        verbose_name = "storm damage"
        verbose_name_plural = "storm damage"

    incident_id = models.IntegerField()
    date = models.DateField()
    incident_start_time = models.TimeField()
    incident_end_time = models.TimeField()
    incident_duration = models.DurationField()
    incident_priority = models.IntegerField(null=True)
    service_area = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    damage_type = models.CharField(max_length=255)
    geometry = models.PointField()


class SoilModel(models.Model):

    class Meta:
        db_table = "incident_predictions_soil"
        verbose_name = "soil information"
        verbose_name_plural = "soil information"

    location = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    soil_function = models.CharField(max_length=255)
    geometry = models.MultiPolygonField()


class BuildingsModel(models.Model):

    class Meta:
        db_table = "incident_predictions_buildings"
        verbose_name = "building information"
        verbose_name_plural = "buildings information"

    construction_year = models.IntegerField()
    geometry = models.MultiPolygonField()


class VunerableLocationsModel(models.Model):

    class Meta:
        db_table = "incident_predictions_vunerable_locations"
        verbose_name = "vunerable location"
        verbose_name_plural = "vunerable locations"

    type = models.CharField(max_length=100)
    region = models.CharField(max_length=150)
    name = models.CharField(max_length=255)
    geometry = models.PointField()


class WeatherDataModel(models.Model):

    WEATHER_MAIN_CHOICES = [
        ("Clear", 'Clear'),
        ("Thunderstorm", 'Thunderstorm'),
        ("Fog", 'Fog'),
        ("Smoke", 'Smoke'),
        ("Haze", 'Haze'),
        ("Snow", 'Snow'),
        ("Rain", 'Rain'),
        ("Mist", 'Mist'),
        ("Drizzle", 'Drizzle'),
        ("Clouds", 'Clouds'),
        ("Squall", 'Squall'),
    ]

    class Meta:
        db_table = "incident_predictions_weather_data"
        verbose_name = "weather data"
        verbose_name_plural = "weather data"

    dt_iso = models.DateTimeField()
    temp = models.FloatField()
    dew_point = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_deg = models.IntegerField()
    wind_gust = models.FloatField()
    rain_1h = models.FloatField()
    rain_3h = models.FloatField()
    snow_1h = models.FloatField()
    weather_main = models.CharField(max_length=15, choices=WEATHER_MAIN_CHOICES)


class WeatherMainPriority(models.Model):

    class Meta:
        db_table = "incident_predictions_weather_main_priority"
        verbose_name = "weather data priority"
        verbose_name_plural = "weather data priorities"

    weather_main = models.CharField(max_length=50, unique=True)
    weather_priority = models.IntegerField()


class TreeTypeTranslations(models.Model):

    class Meta:
        db_table = "incident_predictions_tree_type_translations"
        verbose_name = "tree type translation"
        verbose_name_plural = "tree type translations"

    dutch_name = models.CharField(max_length=150, unique=True)
    english_name = models.CharField(max_length=150)


class PredictiveModels(models.Model):

    class Meta:
        verbose_name = "predictive model"
        verbose_name_plural = "predictive models"

    MODEL_TYPES = [
        ('COUNT', 'COUNT'),
        ('CLASSIFICATION', 'CLASSIFICATION'),
        ('PROBABILITY', 'PROBABILITY'),
        ('OTHER', 'OTHER'),
    ]

    name = models.CharField(max_length=150)
    version = models.CharField(max_length=10)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    file = models.FileField()


class ServiceAreas(models.Model):

    location = models.CharField(max_length=255)
    municipality = models.CharField(max_length=50)
    geometry = models.PointField()
