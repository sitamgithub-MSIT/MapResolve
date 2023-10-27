"""
This module contains forms for user authentication and profile creation/updation.

The module contains the following classes:
    - MyUserCreationForm: A form for creating new users, including all the required fields plus a reCAPTCHA field.
    - AuthForm: A form for authenticating users.
    - UserProfileForm: A form for creating or updating a user's profile information.
"""
# Django imports
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

# Local imports
from .models import UserProfile


# Form for the User Creation model
class MyUserCreationForm(UserCreationForm):
    """
    A form for creating new users, including all the required
    fields plus a reCAPTCHA field.

    Attributes:
        first_name (CharField): A field for the user's first name.
        last_name (CharField): A field for the user's last name.
        username (EmailField): A field for the user's email address.
        password1 (CharField): A field for the user's password.
        password2 (CharField): A field for confirming the user's password.
        token (CharField): A hidden field for the reCAPTCHA token.
    """

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "*Your first name.."}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "*Your last name.."}),
    )
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "*Your email address.."}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "*Password..", "class": "password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "*Confirm Password..", "class": "password"}
        )
    )

    # reCAPTCHA field
    token = forms.CharField(widget=forms.HiddenInput())

    # Meta class for the User model
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")


# Form for the User Authentication form
class AuthForm(AuthenticationForm):
    """
    A form for authenticating users.

    Inherits from Django's built-in AuthenticationForm and adds custom fields for email and password input.

    Attributes:
        username (EmailField): A field for the user's email address.
        password (CharField): A field for the user's password.
    """

    # Fields for the User Authentication form
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "*Your email address.."}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "*Password..", "class": "password"}
        )
    )

    # Meta class for the User Authentication model
    class Meta:
        model = User
        fields = ("username", "password")


# Form for the User Profile form
class UserProfileForm(forms.ModelForm):
    """
    A form for creating or updating a user's profile information.

    Includes fields for the user's address, town, county, postcode, country, longitude, and latitude.

    Inherits from Django's built-in ModelForm class and uses the UserProfile model.
    """

    # Char fields for the Profile form
    address = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    town = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    county = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    postcode = forms.CharField(max_length=8, required=True, widget=forms.HiddenInput())
    country = forms.CharField(max_length=40, required=True, widget=forms.HiddenInput())
    longitude = forms.CharField(
        max_length=50, required=True, widget=forms.HiddenInput()
    )
    latitude = forms.CharField(max_length=50, required=True, widget=forms.HiddenInput())

    # Meta class for the User Profile model
    class Meta:
        model = UserProfile
        fields = (
            "address",
            "town",
            "county",
            "postcode",
            "country",
            "longitude",
            "latitude",
        )
