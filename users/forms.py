# Django imports
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

# Local imports
from .models import UserProfile


# Form for the User Creation model
class MyUserCreationForm(UserCreationForm):
    # Fields for the User Creation form
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