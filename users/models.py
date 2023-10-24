# Importing the models module
from django.db import models

# Importing the User model from django.contrib.auth.models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    # Fields for the Profile model

    # Auto generated fields
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # One to one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Char fields
    address = models.CharField(
        verbose_name="Address", max_length=100, null=True, blank=True
    )
    town = models.CharField(
        verbose_name="Town/City", max_length=100, null=True, blank=True
    )
    county = models.CharField(
        verbose_name="County", max_length=100, null=True, blank=True
    )
    postcode = models.CharField(
        verbose_name="Post Code", max_length=8, null=True, blank=True
    )
    country = models.CharField(
        verbose_name="Country", max_length=100, null=True, blank=True
    )
    longitude = models.CharField(
        verbose_name="Longitude", max_length=50, null=True, blank=True
    )
    latitude = models.CharField(
        verbose_name="Latitude", max_length=50, null=True, blank=True
    )

    # Float fields
    captcha_score = models.FloatField(default=0.0)

    # Boolean fields
    has_profile = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # String representation of the Profile model
    def __str__(self):
        return f"{self.user}"
