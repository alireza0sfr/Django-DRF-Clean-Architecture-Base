from django.db.models import QuerySet, Q
from django.utils import timezone

from domain.apps.identity.models import IPBan, UserBan
from infrastructure.repositories.generic import GenericRepository
from infrastructure.serializers.identity.serializers import UserBanModelSerializer, IPBanModelSerializer


class UserBanRepository(GenericRepository):
    model = UserBan
    serializer_class = UserBanModelSerializer

    def get_actives(self, serialize=True) -> QuerySet:
        result = self.filter(Q(until__gt=timezone.now()))
        return self.serializer_class(result, many=True).data if serialize else result


class IPBanRepository(GenericRepository):
    model = IPBan
    serializer_class = IPBanModelSerializer

    def get_actives(self, serialize=True) -> QuerySet:
        result = self.filter(Q(until__gt=timezone.now()))
        return self.serializer_class(result, many=True).data if serialize else result
