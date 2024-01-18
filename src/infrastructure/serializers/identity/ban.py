from rest_framework.serializers import ModelSerializer

from domain.apps.identity.models import User, UserBan, IPBan
from infrastructure.exceptions.exceptions import EntityNotFoundException

from .user import UserModelSerializer 

class UserBanModelSerializer(ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = UserBan
        fields = ['id', 'user', 'until', 'reason', 'description', 'created_date']
        read_only_fields = ['id', 'created_date']

    def create(self, validated_data):
        user_data = self.initial_data.pop('user')

        try:
            user = User.objects.get(id=user_data.get('id'))
        except User.DoesNotExist:
            raise EntityNotFoundException(message='User Not Found!')

        response = UserBan.objects.create(user=user, **validated_data)
        
        return response


class IPBanModelSerializer(ModelSerializer):
    class Meta:
        model = IPBan
        fields = ['id', 'ip', 'until', 'reason', 'description', 'created_date']
        read_only_fields = ['id', 'created_date']