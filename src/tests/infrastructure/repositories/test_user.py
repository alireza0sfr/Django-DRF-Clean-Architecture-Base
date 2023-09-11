import pytest
import factory

from django.utils import timezone
from django.db.models import Q

from domain.enums.identity.enum import BanReasons
from application.dtos.identity.user import UserDto
from application.dtos.identity.ban import UserBanDto
from infrastructure.repositories.identity.user import UserRepository
from tests.base import BaseTest
from tests.factories.identity import UserFactory

@pytest.mark.django_db
class TestUserRepository(BaseTest):

    def test_get(self):
        # Arrange
        user = UserFactory()
        repository = UserRepository()

        # Act
        response = repository.get(Q(id=str(user.id)))

        # Assert
        assert str(response.id) == str(user.id)

    def test_filter(self):
        # Arrange
        count = 3
        users = UserFactory.create_batch(count)
        repository = UserRepository()

        # Act
        response = repository.filter(Q(is_active=users[0].is_active))

        # Assert
        assert len(response) >= len(users)

    def test_get_by_pk(self):
        # Arrange
        user = UserFactory()
        repository = UserRepository()

        # Act
        response = repository.get_by_pk(pk=user.id)

        # Assert
        assert str(response.id) == str(user.id)

    def test_create(self):
        # Arrange
        user = factory.build(dict, FACTORY_CLASS=UserFactory)
        repository = UserRepository()
        dto = UserDto(**user)

        # Act
        response = repository.create(dto=dto)

        # Assert
        assert response.username == dto.username
        assert response.email == dto.email

    def test_bulk_create(self):
        # Arrange
        user1 = factory.build(dict, FACTORY_CLASS=UserFactory)
        user2 = factory.build(dict, FACTORY_CLASS=UserFactory)
        repository = UserRepository()
        dtos = [UserDto(**user1), UserDto(**user2)]

        # Act
        response = repository.bulk_create(dtos=dtos)

        # Assert
        assert response[0].username == dtos[0].username
        assert response[0].email == dtos[0].email
        assert response[1].username == dtos[1].username
        assert response[1].email == dtos[1].email

    def test_delete(self):
        # Arrange
        user = UserFactory()
        repository = UserRepository()

        # Act
        response = repository.delete(Q(id=user.id))

        # Assert
        assert response[0] >= 1

    def test_bulk_delete(self):
        # Arrange
        user1 = UserFactory()
        user2 = UserFactory()
        repository = UserRepository()

        # Act
        response = repository.delete(Q(id__in=[user1.id, user2.id]))

        # Assert
        assert response[0] >= 2

    def test_update(self):
        # Arrange
        user = factory.build(dict, FACTORY_CLASS=UserFactory)
        repository = UserRepository()
        dto = UserDto(**user)

        # Act
        created = repository.create(dto=dto)
        dto.id = created.id
        dto.email = 'updated@test.org'
        response = repository.update(dto=dto)

        # Assert
        assert response.email == dto.email
        assert response.email != created.email

    def test_partial_update(self):
        # Arrange
        user = UserFactory()
        data = {'email': 'updated@test.org'}

        # Act
        repository = UserRepository()
        response = repository.partial_update(user.id, data)

        # Assert
        assert response.email == data.get('email')
        assert response.email != user.email