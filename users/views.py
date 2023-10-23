# Django imports
from django.shortcuts import redirect, render 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Local imports
from .forms import MyUserCreationForm, AuthForm, UserProfileForm

# Create your views here.
