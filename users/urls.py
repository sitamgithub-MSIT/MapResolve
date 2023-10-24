# Importing the path function from django.urls
from django.urls import path

# Importing the views.py file from the users app
from . import views

# Setting the app_name variable to "users"
app_name = "users"

# Setting the urlpatterns variable to a list of paths
urlpatterns = [
    # Path for the Account view
    path("account/", views.AccountView.as_view(), name="account"),
    # Path for the Profile view
    path("profile/", views.profile_view, name="profile"),
    # Path for the Register view
    path("register/", views.RegisterView.as_view(), name="register"),
    # Path for the Login view
    path("login/", views.LoginView.as_view(), name="login"),
    # Path for the Logout view
    path("logout/", views.LogoutView.as_view(), name="logout"),
]