from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from presentation.controllers.identity.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('jwt/generate/', CustomTokenObtainPairView.as_view(), name='jwt-generate'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify')
]
