# Django imports
from django.shortcuts import render, redirect, reverse
from django.conf import settings

# Local imports
from djangomaps.mixins import Directions


# Create your views here.


# Function based view for the routing
def routing(request):
    # Getting the context
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "base_country": settings.BASE_COUNTRY,
    }

    # Returning the response
    return render(request, "main/path.html", context)


# Function based view for displaying a map
def maps_view(request):
    # Getting the params
    lat_a = request.GET.get("lat_a")
    long_a = request.GET.get("long_a")
    lat_b = request.GET.get("lat_b")
    long_b = request.GET.get("long_b")
    lat_c = request.GET.get("lat_c")
    long_c = request.GET.get("long_c")
    lat_d = request.GET.get("lat_d")
    long_d = request.GET.get("long_d")

    if lat_a and long_a and lat_b and long_b and lat_c and long_c and lat_d and long_d:
        # Getting the directions
        directions = Directions(
            lat_a=lat_a,
            long_a=long_a,
            lat_b=lat_b,
            long_b=long_b,
            lat_c=lat_c,
            long_c=long_c,
            lat_d=lat_d,
            long_d=long_d,
        )
    else:
        # Redirecting to the routing page
        return redirect(reverse("main:routing"))

    # Getting the context
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "base_country": settings.BASE_COUNTRY,
        "lat_a": lat_a,
        "long_a": long_a,
        "lat_b": lat_b,
        "long_b": long_b,
        "lat_c": lat_c,
        "long_c": long_c,
        "lat_d": lat_d,
        "long_d": long_d,
        "origin": f"{lat_a},{long_a}",
        "destination": f"{lat_b},{long_b}",
        "directions": directions,
    }

    # Returning the response
    return render(request, "main/map.html", context)
