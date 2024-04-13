"""
This module registers the UserProfile model with the Django admin site.
"""

from django.contrib import admin
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
