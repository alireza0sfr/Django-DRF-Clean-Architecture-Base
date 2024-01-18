from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField

from domain.apps.identity.models import User

class UserModelSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_active', 'is_verified', 'is_superuser', 'is_staff', 'is_hidden', 'created_date']
        read_only_fields = ['id', 'date_joined', 'is_active', 'is_verified', 'is_superuser', 'is_staff', 'is_hidden', 'created_date']


class UserRegisterSerializer(Serializer):
    username = CharField(max_length=255)
    email = EmailField(max_length=255, allow_blank=True)
    password = CharField()
