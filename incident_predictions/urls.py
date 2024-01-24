"""
URL configuration for storm_incidents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from incident_predictions.views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("load_data/high_ground_water", load_high_ground_water, name="load_high_ground_water"),
    path("load_data/tree_data", load_tree_data, name="load_tree_data"),
    path("load_data/load_grid", load_grid, name="load_grid"),
    path("load_data/load_incidents", load_incidents, name="load_incidents"),
    path("load_data/load_soil", load_soil, name="load_soil"),
    path("load_data/load_buildings", load_buildings, name="load_buildings"),
    path("load_data/load_vunerable_locations", load_vunerable_locations, name="load_vunerable_locations"),
    path("load_data/load_weather_data", load_weather_data, name="load_weather_data"),
    path("weather_predictions", weather_predictions, name="weather_predictions"),

]
