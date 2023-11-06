"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from decouple import config

from presentation.controllers.sample import SampleViewSet
from presentation.controllers.honeypot.views import HoneypotLoginView

BASENAME = "api"

urlpatterns = [
    path(
        f"{BASENAME}/v1.0/authentication/",
        include("presentation.api.authentication.urls"),
    ),
    path(f"{BASENAME}/v1.0/identity/", include("presentation.api.identity.urls")),
    path(f"{BASENAME}/v1.0/", include("presentation.api.v1.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]

development_urls = [
    path("admin/", admin.site.urls),
    path("test/", SampleViewSet.as_view({"get": "retrieve"}, name="test")),
]
production_urls = [
    path(f'{config("ADMIN_SECURE_LOGIN_ROUTE")}/', admin.site.urls),
    path("admin/", HoneypotLoginView.as_view(), name="honeypot-login"),
]

if settings.DEBUG:
    urlpatterns += development_urls
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += production_urls


handler400 = "presentation.controllers.base.custom_error_400"  # bad_request
handler403 = "presentation.controllers.base.custom_error_403"  # permission_denied
handler404 = "presentation.controllers.base.custom_error_404"  # page_not_found
handler500 = "presentation.controllers.base.custom_error_500"  # server_error
