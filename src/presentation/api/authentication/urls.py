from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from presentation.controllers.identity.views import AuthenticationViewSet


router = DefaultRouter()
router.register('users', AuthenticationViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('jwt/generate/', TokenObtainPairView.as_view(), name='jwt-generate'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify')
]
