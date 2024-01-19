from django.contrib import admin
from incident_predictions import models, database_views
# Register your models here.


admin.site.register(database_views.CountTreeDiameterView)
admin.site.register(database_views.UnderWaterPercentageOverlapView)
admin.site.register(database_views.SoilPercentageOverlapView)
admin.site.register(database_views.TreeAgeDescription)
admin.site.register(database_views.CountTreeHeightView)


@admin.register(models.WeatherMainPriority)
class WeatherMainPriorityAdmin(admin.ModelAdmin):
    list_display = ("weather_main", "weather_priority")


@admin.register(models.TreeTypeTranslations)
class TreeTypeTranslationsAdmin(admin.ModelAdmin):
    list_display = ("dutch_name", "english_name")


@admin.register(models.HighGroundWaterModel)
class HighGroundWaterModelAdmin(admin.ModelAdmin):

    list_display = ('location','drainage','geometry')


@admin.register(models.TreesModel)
class TreesModelAdmin(admin.ModelAdmin):

    list_display = (
        'tree_id','species_name','species_name_short',
        'species_name_nl','species_name_top',
        'tree_height','trunk_diameter_class',
        'plant_year','tree_age','predicted_age',
        'tree_type','location_detailed',
        'type_manager',
        'type_owner')


@admin.register(models.AmsterdamGridModel)
class AmsterdamGridModelAdmin(admin.ModelAdmin):

    list_display = ('id', 'grid_id')


@admin.register(models.StormDamageModel)
class StormDamageModelAdmin(admin.ModelAdmin):

    list_display = (
        'incident_id',
        'date',
        'incident_start_time',
        'incident_end_time',
        'incident_duration',
        'incident_priority',
        'service_area',
        'municipality',
        'damage_type'
    )


@admin.register(models.SoilModel)
class SoilModelAdmin(admin.ModelAdmin):
    list_display = (
        'location',
        'zone',
        'soil_function'
    )


@admin.register(models.BuildingsModel)
class BuildingsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'construction_year')


@admin.register(models.VunerableLocationsModel)
class VunerableLocationsModelAdmin(admin.ModelAdmin):
    list_display = ('type', 'region', 'name')


@admin.register(models.WeatherDataModel)
class WeatherDataModelAdmin(admin.ModelAdmin):
    list_display = (
        'dt_iso',
        'temp',
        'temp_min',
        'temp_max',
        'pressure',
        'humidity',
        'wind_speed',
        'wind_deg',
        'wind_gust',
        'weather_main'
)
