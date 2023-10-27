"""
This module contains mixins and functions for Django views.

The module contains the following:
- FormErrorsMixin: A mixin that returns error messages for a form.
- recaptchavalidate: A function that validates a reCAPTCHA token using the Google API.
- urlappend: A function that appends query parameters to a URL and returns a redirect response.
- AjaxFormMixin: A mixin for handling AJAX form submissions.
- Directions: A function that takes in latitude and longitude coordinates for two points (origin and destination) and optionally for two waypoints. It then uses the Google Maps API to get the directions between the points and returns the distance, duration and route steps as a dictionary.
"""

# Importing from Django modules
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.utils.timesince import timesince

# Other imports
import json
import requests
import datetime
from urllib.parse import urlencode
from humanfriendly import format_timespan

# Importing from Django modules
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.utils.timesince import timesince

# Other imports
import json
import requests
import datetime
from urllib.parse import urlencode
from humanfriendly import format_timespan


# Form errors checking
def FormErrorsMixin(*args):
    """
    A mixin that returns error messages for a form.

    Args:
        *args: A variable-length argument list of form fields.

    Returns:
        str: A string containing error messages for the form fields.
    """
    message = ""

    for f in args:
        if f.errors:
            message = f.errors.as_text()

    return message


# Method for the recaptcha validation
def recaptchavalidate(token):
    """
    Validates a reCAPTCHA token using the Google API.

    Args:
        token (str): The reCAPTCHA token to validate.

    Returns:
        dict: A dictionary containing the response from the Google API.
    """
    # Sending the request to the Google API
    return requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": token},
    ).json()


# Method for the url appending with the params
def urlappend(**kwargs):
    """
    Appends query parameters to a URL and returns a redirect response.

    Args:
        url (str): The URL to append the query parameters to.
        params (dict): The query parameters to append to the URL.

    Returns:
        A redirect response with the query parameters appended to the URL.
    """
    # Getting the url and the params
    url = kwargs.get("url")
    params = kwargs.get("params")

    # The response
    response = redirect(url)

    # Appending the params to the url
    if params:
        query_string = urlencode(params)
        response["Location"] += f"?{query_string}"

    # Returning the response
    return response


# Class for the Ajax form reponse
class AjaxFormMixin(object):
    """
    A mixin for handling AJAX form submissions.

    This mixin provides methods for handling form validation and invalidation
    when the form is submitted via AJAX. It checks for the presence of the
    "x-requested-with" header in the request, and returns a JSON response
    containing the result of the form submission.
    """

    # Method for the form invalidation
    def form_invalid(self, form):
        """
        Handle an invalid form submission.

        This method is called when the form submission is invalid. It returns
        a JSON response containing the form errors if the request was made via
        AJAX, otherwise it returns the default response from the parent class.
        """
        response = super(AjaxFormMixin, self).form_invalid(form)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            message = FormErrorsMixin(form)
            return JsonResponse({"result": "Error", "message": message})

        return response

    # Method for the form validation
    def form_valid(self, form):
        """
        Handle a valid form submission.

        This method is called when the form submission is valid. It returns
        a JSON response containing the success message if the request was made
        via AJAX, otherwise it returns the default response from the parent class.
        """
        response = super(AjaxFormMixin, self).form_valid(form)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            form.save()
            return JsonResponse({"result": "Success", "message": ""})

        return response


# Method handling directions from Google Maps API
def Directions(*args, **kwargs):
    """
    This function takes in latitude and longitude coordinates for two points (origin and destination) and optionally for two waypoints.
    It then uses the Google Maps API to get the directions between the points and returns the distance, duration and route steps as a dictionary.

    Args:
        lat_a (float): Latitude of the origin point.
        long_a (float): Longitude of the origin point.
        lat_b (float): Latitude of the destination point.
        long_b (float): Longitude of the destination point.
        lat_c (float, optional): Latitude of the first waypoint. Defaults to None.
        long_c (float, optional): Longitude of the first waypoint. Defaults to None.
        lat_d (float, optional): Latitude of the second waypoint. Defaults to None.
        long_d (float, optional): Longitude of the second waypoint. Defaults to None.

    Returns:
        dict: A dictionary containing the origin, destination, distance, duration and route steps.
    """
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
        for route in range(len(routes)):
            # Adding the distance and duration
            distance += int(routes[route]["distance"]["value"])
            duration += int(routes[route]["duration"]["value"])

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
            "duration": timesince(duration),
            "route": routes_list,
        }
