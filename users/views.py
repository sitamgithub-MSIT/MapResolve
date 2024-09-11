"""
This module contains views for user authentication and registration.
It includes the following classes and functions:
    - AccountView: A view that displays the account page for a logged-in user.
    - profile_view: A view function for the user profile page.
    - LoginView: A view for user login.
    - RegisterView: A view for user registration.
"""

# Django imports
from django.shortcuts import redirect, render, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Local imports
from .forms import MyUserCreationForm, AuthForm, UserProfileForm
from djangomaps.mixins import (
    FormErrorsMixin,
    AjaxFormMixin,
    urlappend,
    recaptchavalidate,
)

# Create your views here.

result = "Error"
message = "Something went wrong!"


# Class for the Account view
class AccountView(TemplateView):
    """
    A view that displays the account page for a logged-in user.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = "users/account.html"

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


# Method for the Profile view
def profile_view(request):
    """
    View function for the user profile page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Getting the user
    user = request.user

    # Getting the user profile
    profile = user.userprofile

    # Getting the user profile form
    form = UserProfileForm(instance=profile)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = UserProfileForm(request.POST, instance=profile)

        result = "Error"
        message = "Something went wrong!"

        if form.is_valid():
            # Saving the form
            obj = form.save()
            obj.has_profile = True
            obj.save()

            # Success message
            result = "Success"
            message = "Profile updated successfully!"

        else:
            # Error message
            message = FormErrorsMixin(form)

        data = {"result": result, "message": message}
        return JsonResponse(data)

    else:
        # Context data for the Profile view
        context = {
            "form": form,
        }

        context["google_api_key"] = settings.GOOGLE_API_KEY
        context["base_country"] = settings.BASE_COUNTRY

    # Returning the response
    return render(request, "users/profile.html", context)


# Class for the User Login view
class LoginView(AjaxFormMixin, FormView):
    """
    A view for user login.

    Attributes:
        - template_name (str): The name of the template to be used for rendering the view.
        - form_class (class): The form class to be used for rendering the view.
        - success_url (str): The URL to redirect to after a successful login.

    Methods:
        form_valid(form): Handles the form submission and logs in the user if the form is valid.
    """

    template_name = "users/login.html"
    form_class = AuthForm
    success_url = "/"

    def form_valid(self, form):
        """
        Handles the form submission and logs in the user if the form is valid.

        Args:
            form (AuthForm): The form instance containing the submitted data.

        Returns:
            response (JsonResponse): A JSON response containing the result of the login attempt.
        """
        response = super(AjaxFormMixin, self).form_valid(form)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
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

                result = "Success"
                message = "Login successful!"

            else:
                # Error message
                message = FormErrorsMixin(form)

            # Json data to be returned to the ajax call
            data = {"result": result, "message": message}
            return JsonResponse(data)

        # Returning the response
        return response


# Class for the User Registration view
class RegisterView(AjaxFormMixin, FormView):
    """
    View for user registration.

    Inherits from AjaxFormMixin and FormView.
    Uses MyUserCreationForm as the form class.
    On successful registration, logs in the user and returns a success message.
    """

    # Template for the User Registration view
    template_name = "users/register.html"

    # Form class for the User Registration view
    form_class = MyUserCreationForm
    success_url = "/"

    # context data for the User Registration view
    def get_context_data(self, **kwargs):
        # Getting the context data
        context = super().get_context_data(**kwargs)
        # Adding the recaptcha key to the context data
        context["recaptcha_site_key"] = settings.RECAPTCHA_PUBLIC_KEY

        # Returning the context
        return context

    # Method for the User Registration view
    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            # Getting the form data
            token = form.cleaned_data.get("token")

            # Validating the recaptcha
            result = recaptchavalidate(token)

            if result["success"]:
                # Creating the user
                user = form.save()
                user.email = user.username
                user.save()

                up = user.userprofile
                up.captcha_score = result["score"]
                up.save()

                # Logging in the user
                login(
                    self.request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )

                # Success message
                result = "Success"
                message = "Registration successful!"

            # Json data to be returned to the ajax call
            data = {"result": result, "message": message}
            return JsonResponse(data)

        # Returning the response
        return response


# Method for the User Logout view
# class LogoutView(TemplateView):
#     # Template for the User Logout view
#     template_name = ""

#     # Method for the User Logout view
#     def get(self, request, *args, **kwargs):
#         # Logging out the user
#         logout(request)

#         # Redirecting to the home page
#         return redirect(reverse("users:login"))


def logout_view(request):
    """
    Logs out the user and redirects to the sign-in page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the sign-in page.
    """
    # Logging out the user
    logout(request)

    # Redirecting to the sign-in page
    return redirect(reverse("users:login"))
