from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from application.dtos.accounts.ban import UserBanDto
from infrastructure.repositories.accounts.ban import UserBanRepository
from infrastructure.repositories.generic import GenericRepository

User = get_user_model()


class UserRepository(GenericRepository):
    model = User
    user_ban_repository = UserBanRepository()

    def ban(self, user, until, reason, description):
        dto = UserBanDto(user=user, until=until, reason=reason, description=description)
        entity = self.mapper.map(dto, self.user_ban_repository.model)
        return self.user_ban_repository.create(entity)

    def try_unban(self, user):
        return self.user_ban_repository.delete(Q(user=user, until__gt=timezone.now()))
