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
    # Template for the Account view
    template_name = "users/account.html"

    # Method for the Account view
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


# Method for the Profile view
def profile_view(request):
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
    # Template for the User Login view
    template_name = "users/login.html"

    # Form class for the User Login view
    form_class = AuthForm
    success_url = "/"

    # Method for the User Login view
    def form_valid(self, form):
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

    # Logging out the user
	logout(request)

    # Redirecting to the sign-in page
	return redirect(reverse('users:login'))


