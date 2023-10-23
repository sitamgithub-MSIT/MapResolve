# Django imports
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Local imports
from .forms import MyUserCreationForm, AuthForm, UserProfileForm
from djangomaps.mixins import (
    FormErrorsMixin,
    AjaxFormMixin,
    urlappend,
    recaptchavalidate,
)

# Create your views here.


# Class for the User Login view
class LoginView(FormView):
    # Template for the User Login view
    template_name = "#"

    # Form class for the User Login view
    form_class = AuthForm
    success_url = "/"

    # Method for the User Login view
    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)

        if self.request.is_ajax():
            # Getting the form data
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Authenticating the user
            user = authenticate(self.request, username=username, password=password)

            if user is not None:
                # Logging in the user
                login(
                    self.request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )

                result = "success"
                message = "Login successful!"

            else:
                # Error message
                message = FormErrorsMixin(form)

            # Json data to be returned to the ajax call
            data = {"result": result, "message": message}
            return JsonResponse(data)

        # Returning the response
        return response


# # Class for the User Registration view

# class RegisterView(FormView):
#     # Template for the User Registration view
#     template_name = "users/register.html"

#     # Form class for the User Registration view
#     form_class = MyUserCreationForm

#     # Method for the User Registration view
#     def form_valid(self, form):
#         # Getting the form data
#         name = form.cleaned_data.get("name")
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password1")

#         # Creating the user
#         user = User.objects.create_user(
#             username=username, email=email, password=password
#         )

#         # Creating the profile
#         profile = Profile.objects.create(user=user)

#         # Logging in the user
#         login(self.request, user)

#         # Returning the response
#         return redirect("users:profile", username=username)
