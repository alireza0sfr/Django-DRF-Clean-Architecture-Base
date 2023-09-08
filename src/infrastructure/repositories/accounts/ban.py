from domain.apps.accounts.models import IPBan, UserBan
from infrastructure.repositories.generic import GenericRepository
from infrastructure.serializers.accounts.serializers import UserBanModelSerializer, IPBanModelSerializer

class UserBanRepository(GenericRepository):
    model = UserBan
    serializer_class = UserBanModelSerializer


class IPBanRepository(GenericRepository):
    model = IPBan
    serializer_class = IPBanModelSerializer
