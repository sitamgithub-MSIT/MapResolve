"""
URL configuration for djangomaps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Set the urlpatterns variable to a list of paths
urlpatterns = [
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("mapresolve_admin_secret/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("", include("users.urls", namespace="users")),
    path("silk/", include("silk.urls", namespace="silk")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
