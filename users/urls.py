"""
This module contains the URL patterns for the users app.

It imports the path function from django.urls and the views.py file from the users app.
It sets the app_name variable to "users" and the urlpatterns variable to a list of paths.
"""

from django.urls import path
from . import views

# Set the app_name as "users"
app_name = "users"

# Set the urlpatterns variable to a list of paths
urlpatterns = [
    path("", views.AccountView.as_view(), name="account"),
    path("profile", views.profile_view, name="profile_view"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout_view"),
]
