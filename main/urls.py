"""
This module defines the URL patterns for the main app.

It imports the path function from django.urls and the views.py file from the main app.
It sets the app_name variable to "main" and the urlpatterns variable to a list of paths.
"""

from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("route", views.routing, name="routing"),
    path("map", views.maps_view, name="maps_view"),
]
