from django.contrib.gis.db import models


class Buildings(models.Model):
    CONSTRUCTION_YEAR = models.IntegerField()
    geometry = models.PolygonField()


class HighGroundWaterModel(models.Model):

    DRAINAGE_CHOICES = [
        ('DRAIN_POSSIBLE', 'DRAIN_POSSIBLE'),
        ('DRAIN_NOT_POSSIBLE', 'DRAIN_NOT_POSSIBLE'),
    ]

    location = models.CharField(max_length=200)
    drainage = models.CharField(max_length=20, choices=DRAINAGE_CHOICES)
    geometry = models.MultiPolygonField()


class TreesModel(models.Model):

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

    grid_id = models.CharField(max_length=255, null=False)
    geometry = models.PolygonField()


class StormDamageModel(models.Model):

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

    area_number = models.IntegerField()
    location = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    zone_road = models.CharField(max_length=255)
    soil_function = models.CharField(max_length=255)
    layer_0_05_meters = models.CharField(max_length=255)
    layer_05_1_meters = models.CharField(max_length=255)
    layer_1_2_meters = models.CharField(max_length=255)
    layer_2_meters = models.CharField(max_length=255)
    explanation = models.CharField(max_length=255)
    explanation_road = models.CharField(max_length=255)
    statistical_key_numbers = models.CharField(max_length=255)
    statistical_key_numbers_road = models.CharField(max_length=255)
    geometry = models.MultiPolygonField()
