from rest_framework.serializers import ModelSerializer

from domain.apps.accounts.models import User, UserBan, IPBan

class UserModelSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_active', 'is_verified', 'is_superuser', 'is_staff', 'is_hidden', 'created_date']
        read_only_fields = ['id', 'date_joined', 'is_active', 'is_verified', 'is_superuser', 'is_staff', 'is_hidden', 'created_date']


class UserBanModelSerializer(ModelSerializer):
    user = UserModelSerializer()
    class Meta:
        model = UserBan
        fields = ['id', 'user', 'until', 'reason', 'description', 'created_date']
        read_only_fields = ['id', 'created_date']
        
class IPBanModelSerializer(ModelSerializer):
    class Meta:
        model = IPBan
        fields = ['id', 'ip', 'until', 'reason', 'description', 'created_date']
        read_only_fields = ['id', 'created_date']