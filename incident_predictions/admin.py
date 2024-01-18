from django.contrib import admin
from incident_predictions import models, database_views
# Register your models here.


admin.site.register(database_views.CountTreeDiameterView)
admin.site.register(database_views.UnderWaterPercentageOverlapView)
admin.site.register(database_views.SoilPercentageOverlapView)
admin.site.register(database_views.TreeAgeDescription)
admin.site.register(database_views.CountTreeHeightView)

admin.site.register(models.BuildingsModel)
admin.site.register(models.SoilModel)
admin.site.register(models.TreesModel)
admin.site.register(models.WeatherDataModel)
