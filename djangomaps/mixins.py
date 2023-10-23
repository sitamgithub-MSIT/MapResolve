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
