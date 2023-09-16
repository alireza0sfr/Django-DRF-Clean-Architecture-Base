from rest_framework.response import Response
from django.db.models import Q
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework import status
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from infrastructure.commands.identity.user import UserCommand
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

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = UserCommand()
        response = command.create(request.data)

        login = settings.DJOSER.get('LOGIN_ON_REGISTER')

        if login:
            token_service = TokenService()
            token = token_service.generate(User.objects.get(pk=response.get('id')))
            return Response(data={'data': token}, status=status.HTTP_201_CREATED) 

        else:
            return Response(data={'data': response}, status=status.HTTP_201_CREATED)
    

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