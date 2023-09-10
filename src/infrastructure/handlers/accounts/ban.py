from infrastructure.handlers.base import BaseHandler
from infrastructure.repositories.accounts.ban import UserBanRepository, IPBanRepository
from infrastructure.serializers.accounts.serializers import IPBanModelSerializer, UserBanModelSerializer


class IPBanHandler(BaseHandler):
    repository = IPBanRepository
    serializer_class = IPBanModelSerializer


class UserBanHandler(BaseHandler):
    repository = UserBanRepository
    serializer_class = UserBanModelSerializer

