import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from infrastructure.exceptions.exceptions import UserIsNotActiveException
from infrastructure.services.token import TokenService
from infrastructure.serializers.identity.serializers import UserModelSerializer
from tests.factories.identity import UserFactory
from tests.base import BaseTest

User = get_user_model()


@pytest.mark.django_db
class TestJWTAPI(BaseTest):

    def test_generate_token_for_not_active_user(self):
        # Arrange
        endpoint = reverse('jwt-generate')
        username = 'admin-test'
        password = '@123456!'
        email = 'test@test.com'
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

        # Act
        response = self.api_client.post(endpoint, data={'username': user.username, 'password': password})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('key') == UserIsNotActiveException().key

    def test_generate_token_for_active_user(self):
        # Arrange
        endpoint = reverse('jwt-generate')
        username = 'admin-test'
        password = '@123456!'
        email = 'test@test.com'
        user = User.objects.create_user(username=username, password=password, email=email, is_active=True)

        # Act
        response = self.api_client.post(endpoint, data={'username': username, 'password': password})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('access')
        assert response.data.get('refresh')
        assert response.data.get('user')

    def test_refresh_token_for_not_active_user(self):
        # Arrange
        endpoint = reverse('jwt-refresh')

        username = 'admin-test'
        password = '@123456!'
        email = 'test@test.com'
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

        token_service = TokenService()
        token = token_service.generate(user)

        # Act
        response = self.api_client.post(endpoint, data={'refresh': token.get('refresh_token')})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('key') == UserIsNotActiveException().key

    def test_refresh_token_for_active_user(self):
        # Arrange
        endpoint = reverse('jwt-refresh')

        username = 'admin-test'
        password = '@123456!'
        email = 'test@test.com'
        user = User.objects.create_user(username=username, password=password, email=email, is_active=True)

        token_service = TokenService()
        token = token_service.generate(user)

        # Act
        response = self.api_client.post(endpoint, data={'refresh': token.get('refresh_token')})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('access')


@pytest.mark.django_db
class TestAuthenticationAPI(BaseTest):

    def test_users_list(self):
        # Arrange
        endpoint = reverse('users-list')
        normal_user = UserFactory()
        hidden_user = UserFactory(is_hidden=True)

        # Act
        response = self.api_client.get(endpoint)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert str(normal_user.id) in response.data[0].values()
        assert str(hidden_user.id) not in response.data[0].values()