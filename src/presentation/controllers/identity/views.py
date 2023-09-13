from rest_framework.response import Response
from django.db.models import Q
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from infrastructure.exceptions.exceptions import UserIsNotActiveException, EntityNotFoundException
from infrastructure.services.token import TokenService

User = get_user_model()

class AuthenticationViewSet(UserViewSet):
    
    def list(self, request, *args, **kwargs):
        queryset = User.objects.filter(Q(is_hidden=False))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.get(username=request.data.get('username'))
            
            if not user.is_active:
                raise UserIsNotActiveException()
            
            return super().post(request, *args, **kwargs)
        except User.DoesNotExist:
            raise EntityNotFoundException(message='User Not Found!')
        

class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):

        try:
            token_service = TokenService()
            decoded_token = token_service.decode(request.data.get('refresh'))
            user = User.objects.get(id=decoded_token.get('user_id'))
            
            if not user.is_active:
                raise UserIsNotActiveException()
            
            return super().post(request, *args, **kwargs)
        except User.DoesNotExist:
            raise EntityNotFoundException(message='User Not Found!')