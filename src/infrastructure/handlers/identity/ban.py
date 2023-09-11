from infrastructure.handlers.base import BaseHandler
from infrastructure.repositories.identity.ban import UserBanRepository, IPBanRepository
from infrastructure.serializers.identity.serializers import IPBanModelSerializer, UserBanModelSerializer


class IPBanHandler(BaseHandler):
    repository = IPBanRepository
    serializer_class = IPBanModelSerializer


class UserBanHandler(BaseHandler):
    repository = UserBanRepository
    serializer_class = UserBanModelSerializer

