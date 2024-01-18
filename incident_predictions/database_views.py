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
