from django.urls import path, include
from rest_framework.routers import DefaultRouter

from presentation.controllers.identity.views import IdentityModelViewSet

router = DefaultRouter()
router.register('users', IdentityModelViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
]
