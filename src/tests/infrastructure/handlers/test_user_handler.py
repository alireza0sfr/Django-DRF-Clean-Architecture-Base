import pytest
import factory

from django.utils import timezone
from django.db.models import Q

from domain.enums.identity.enum import BanReasons
from application.dtos.identity.user import UserDto
from application.dtos.identity.ban import UserBanDto
from infrastructure.handlers.identity.user import UserHandler
from tests.base import BaseTest
from tests.factories.identity import UserFactory

@pytest.mark.django_db
class TestUserHandler(BaseTest):
    
    def test_get(self):
        # Arrange
        user = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.get(Q(id=str(user.id)))

        # Assert
        assert str(response.get('id')) == str(user.id)

    def test_filter(self):
        # Arrange
        count = 3
        users = UserFactory.create_batch(count)
        handler = UserHandler()

        # Act
        response = handler.filter(Q(is_active=users[0].is_active))

        # Assert
        assert len(response) >= len(users)

    def test_get_by_pk(self):
        # Arrange
        user = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.get_by_pk(pk=user.id)

        # Assert
        assert str(response.get('id')) == str(user.id)

    def test_create(self):
        # Arrange
        user = factory.build(dict, FACTORY_CLASS=UserFactory)
        handler = UserHandler()
        dto = UserDto(**user)

        # Act
        response = handler.create(dto=dto)

        # Assert
        assert response.get('username') == dto.username
        assert response.get('email') == dto.email

    def test_bulk_create(self):
        # Arrange
        user1 = factory.build(dict, FACTORY_CLASS=UserFactory)
        user2 = factory.build(dict, FACTORY_CLASS=UserFactory)
        handler = UserHandler()
        dtos = [UserDto(**user1), UserDto(**user2)]

        # Act
        response = handler.bulk_create(dtos=dtos)

        # Assert
        assert response[0].get('username') == dtos[0].username
        assert response[0].get('email') == dtos[0].email
        assert response[1].get('username') == dtos[1].username
        assert response[1].get('email') == dtos[1].email

    def test_delete(self):
        # Arrange
        user = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.delete(Q(id=user.id))

        # Assert
        assert response[0] >= 1

    def test_bulk_delete(self):
        # Arrange
        user1 = UserFactory()
        user2 = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.delete(Q(id__in=[user1.id, user2.id]))

        # Assert
        assert response[0] >= 2

    def test_update(self):
        # Arrange
        user = factory.build(dict, FACTORY_CLASS=UserFactory)
        handler = UserHandler()
        dto = UserDto(**user)

        # Act
        created = handler.create(dto=dto)
        dto.id = created.get('id')
        dto.email = 'updated@test.org'
        response = handler.update(dto=dto)

        # Assert
        assert response.get('email') == dto.email
        assert response.get('email') != created.get('email')

    def test_partial_update(self):
        # Arrange
        user = UserFactory()
        data = {'email': 'updated@test.org'}

        # Act
        handler = UserHandler()
        response = handler.partial_update(user.id, data)

        # Assert
        assert response.get('email') == data.get('email')
        assert response.get('email') != user.email

    def test_ban(self):
        # Arrange
        user = UserFactory()
        user_handler = UserHandler()
        user_dto = UserDto(id=user.id, email=user.email, username=user.username)
        user_ban_dto = UserBanDto(user=user_dto, reason=BanReasons.ABUSIVE.value, until=timezone.now())

        # Act
        response = user_handler.ban(user_ban=user_ban_dto)

        # Assert
        assert str(response.get('user').get('id')) == str(user_ban_dto.user.id)

    def test_unban(self):
        # Arrange
        user = UserFactory()
        user_handler = UserHandler()
        user_dto = UserDto(id=user.id, email=user.email, username=user.username)
        user_ban_dto = UserBanDto(user=user_dto, reason=BanReasons.ABUSIVE.value, until=timezone.now() + timezone.timedelta(hours=2))
        ban = user_handler.ban(user_ban=user_ban_dto)

        # Act
        response = user_handler.unban(user=user_dto)

        assert response[0] >= 1