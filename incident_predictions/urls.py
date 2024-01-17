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

urlpatterns = [
    path("load_data/high_ground_water", load_high_ground_water, name="load_high_ground_water"),
    path("load_data/tree_data", load_tree_data, name="load_tree_data"),
    path("load_data/load_grid", load_grid, name="load_grid"),
    path("load_data/load_incidents", load_incidents, name="load_incidents"),
    path("load_data/load_soil", load_soil, name="load_soil"),
]
