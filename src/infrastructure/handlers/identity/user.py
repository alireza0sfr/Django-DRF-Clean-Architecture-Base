from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from domain.enums.identity.enum import BanReasons

from application.dtos.identity.user import UserDto
from application.dtos.identity.ban import UserBanDto

from infrastructure.handlers.base import BaseHandler
from infrastructure.repositories.identity.ban import UserBanRepository
from infrastructure.repositories.identity.user import UserRepository
from infrastructure.serializers.identity.serializers import UserModelSerializer


class UserHandler(BaseHandler):
    repository = UserRepository
    serializer_class = UserModelSerializer
    user_ban_repository = UserBanRepository

    def ban(self, user_ban: UserBanDto):
        repository = self.user_ban_repository()
        return repository.create(dto=user_ban)

    def try_unban(self, user: UserDto):
        repository = self.user_ban_repository()
        return repository.delete(Q(user=user, until__gt=timezone.now()))
