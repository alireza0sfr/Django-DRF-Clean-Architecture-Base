from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from domain.enums.accounts.enum import BanReasons

from application.dtos.accounts.user import UserDto
from application.dtos.accounts.ban import UserBanDto

from infrastructure.handlers.base import BaseHandler
from infrastructure.repositories.accounts.ban import UserBanRepository
from infrastructure.repositories.accounts.user import UserRepository
from infrastructure.serializers.accounts.serializers import UserModelSerializer


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
