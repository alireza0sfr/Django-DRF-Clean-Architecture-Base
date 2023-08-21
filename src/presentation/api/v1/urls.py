
from django.urls import path, include
from presentation.api.router import router

urlpatterns = [
    path('', include(router.urls)),
]