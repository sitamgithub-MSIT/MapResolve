# Importing from Django modules
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect

# Other imports
import json
import requests
import datetime
from urllib.parse import urlencode
from humanfriendly import format_timespan


# Form errors checking
def FormErrorsMixin(*args):
    message = ""

    for f in args:
        if f.errors:
            message = f.errors.as_text()

    return message


# Method for the recaptcha validation
def recaptchavalidate(token):
    # Data to be sent to the Google API
    data = {"secret": settings.RECAPTCHA_SECRET_KEY, "response": token}

    # Sending the request to the Google API
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = r.json()

    return result


# Method for the url appending with the params
def urlappend(**kwargs):
    # Getting the url and the params
    url = kwargs.get("url")
    params = kwargs.get("params")

    # The response
    response = redirect(url)

    # Appending the params to the url
    if params:
        query_string = urlencode(params)
        response["Location"] += "?" + query_string

    # Returning the response
    return response


# Class for the Ajax form reponse
class AjaxFormMixin(object):
    # Method for the form invalidation
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)

        if self.request.is_ajax():
            message = FormErrorsMixin(form)
            return JsonResponse({"result": "Error", "message": message})

        return response

    # Method for the form validation
    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)

        if self.request.is_ajax():
            form.save()
            return JsonResponse({"result": "Success", "message": ""})

        return response


# Method handling directions from Google Maps API
def Directions(*args, **kwargs):
    # Getting the params from the kwargs
    lat_a = kwargs.get("lat_a")
    long_a = kwargs.get("long_a")
    lat_b = kwargs.get("lat_b")
    long_b = kwargs.get("long_b")
    lat_c = kwargs.get("lat_c")
    long_c = kwargs.get("long_c")
    lat_d = kwargs.get("lat_d")
    long_d = kwargs.get("long_d")

    # Getting the origin, destination and waypoints
    origin = f"{lat_a},{long_a}"
    destination = f"{lat_b},{long_b}"
    waypoints = f"{lat_c},{long_c}|{lat_d},{long_d}"

    # Getting the directions from the Google Maps API
    result = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json?",
        params={
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints,
            "key": settings.GOOGLE_API_KEY,
        },
    )

    # Json data to be returned
    directions = result.json()

    # If the status is OK
    if directions["status"] == "OK":
        # Getting the routes
        routes = directions["routes"][0]["legs"]

        # Initializing the distance and duration
        distance = 0
        duration = 0
        routes_list = []

        # Getting the distance and duration
        for route in routes:
            # Adding the distance and duration
            distance += route["distance"]["value"]
            duration += route["duration"]["value"]

            # Getting the route step
            route_step = {
                "origin": routes[route]["start_address"],
                "destination": routes[route]["end_address"],
                "distance": routes[route]["distance"]["text"],
                "duration": routes[route]["duration"]["text"],
                "steps": [
                    [
                        s["distance"]["text"],
                        s["duration"]["text"],
                        s["html_instructions"],
                    ]
                    for s in routes[route]["steps"]
                ],
            }

            # Appending the route step to the routes list
            routes_list.append(route_step)

        # Returning the response
        return {
            "origin": origin,
            "destination": destination,
            "distance": f"{round(distance/1000, 2)} Km",
            "duration": format_timespan(duration),
            "route": routes_list,
        }
