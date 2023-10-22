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


# class AjaxFormMixin(object):
#     def form_invalid(self, form):
#         response = super(AjaxFormMixin, self).form_invalid(form)

#         if self.request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#         else:
#             return response

#     def form_valid(self, form):
#         response = super(AjaxFormMixin, self).form_valid(form)

#         if self.request.is_ajax():
#             data = {"message": "Successfully submitted form data."}
#             return JsonResponse(data)
#         else:
#             return response
