from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from domain.enums.accounts.enum import BanReasons

from application.dtos.accounts.user import UserDto
from application.dtos.accounts.ban import UserBanDto

from infrastructure.repositories.accounts.ban import UserBanRepository
from infrastructure.repositories.generic import GenericRepository
from infrastructure.serializers.accounts.serializers import UserModelSerializer

User = get_user_model()


class UserRepository(GenericRepository):
    model = User
    serializer_class = UserModelSerializer
    user_ban_repository = UserBanRepository()

    def ban(self, user: UserDto, until: datetime, reason: BanReasons, description: str):
        dto = UserBanDto(user=user, until=until, reason=reason, description=description)
        return self.user_ban_repository.create(dto=dto)

    def try_unban(self, user):
        return self.user_ban_repository.delete(Q(user=user, until__gt=timezone.now()))