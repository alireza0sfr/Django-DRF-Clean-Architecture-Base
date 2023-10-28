import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status

from tests.factories.identity import UserFactory
from tests.base import BaseTest


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

    def test_user_create(self):
        # Arrange
        endpoint = reverse('users-list')
        request = {'email': 'sample@test.com', 'username': 'sample_user', 'password': '@123456!'}

        # Act
        response = self.api_client.post(endpoint, data=request)

        # Assert
        assert  response.status_code == status.HTTP_201_CREATED

        if settings.DJOSER.get('LOGIN_ON_REGISTER'):
            assert response.data.get('data').get('access_token', '') != ''
            assert response.data.get('data').get('refresh_token', '') != ''
            assert response.data.get('data').get('user').get('email', '') == request.get('email')
            assert response.data.get('data').get('user').get('username', '') == request.get('username')
        else:
            assert response.data.get('data').get('email', '') == request.get('email')
            assert response.data.get('data').get('username', '') == request.get('username')