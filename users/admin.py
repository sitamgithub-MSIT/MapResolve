"""
This module registers the UserProfile model with the Django admin site.
"""

from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserProfile model.

    This class defines the display, filtering, and search options for the UserProfile model in the Django admin interface.

    Attributes:
        list_display (tuple): A tuple of field names to be displayed in the admin list view.
        list_filter (tuple): A tuple of field names to be used for filtering in the admin list view.
        search_fields (list): A list of field names to be used for searching in the admin list view.

    """

    list_display = (
        "user",
        "address",
        "town",
        "county",
        "postcode",
        "country",
        "captcha_score",
        "has_profile",
        "is_active",
    )
    list_filter = ("has_profile", "is_active")
    search_fields = [
        "user__username",
        "user__email",
        "address",
        "town",
        "county",
        "postcode",
        "country",
    ]


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
