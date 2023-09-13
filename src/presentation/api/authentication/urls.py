from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from presentation.controllers.identity.views import AuthenticationViewSet, CustomTokenObtainPairView, CustomTokenRefreshView

router = DefaultRouter()
router.register('users', AuthenticationViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('jwt/generate/', CustomTokenObtainPairView.as_view(), name='jwt-generate'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify')
]
