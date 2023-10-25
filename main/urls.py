# Importing the path function from django.urls
from django.urls import path

# Importing the views.py file from the main app
from . import views

# Setting the app_name variable to "main"
app_name = "main"

# Setting the urlpatterns variable to a list of paths
urlpatterns = [
    path("route", views.routing, name="routing"),
    path("map", views.maps_view, name="maps_view"),
]
