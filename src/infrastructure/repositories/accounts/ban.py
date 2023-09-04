from domain.apps.accounts.models import IPBan, UserBan
from infrastructure.repositories.generic import GenericRepository


class UserBanRepository(GenericRepository):
    model = UserBan


class IPBanRepository(GenericRepository):
    model = IPBan
