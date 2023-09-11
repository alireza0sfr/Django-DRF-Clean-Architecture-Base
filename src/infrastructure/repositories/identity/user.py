from django.contrib.auth import get_user_model
from django.db.models import Q

from infrastructure.repositories.generic import GenericRepository
from infrastructure.serializers.identity.serializers import UserModelSerializer

User = get_user_model()


class UserRepository(GenericRepository):
    model = User
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(Q(is_hidden=False))