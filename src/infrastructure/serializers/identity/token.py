from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JWTTokenObtainPairSerializer
from rest_framework.serializers import Serializer, CharField

from domain.apps.identity.models import User
from infrastructure.exceptions.exceptions import InvalidTokenException, InvalidIdException

from .user import UserModelSerializer

class IdTokenSerializer(Serializer):
    id = CharField()
    token = CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            user = User.objects.get(pk=self.initial_data.get("id", ""))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise InvalidIdException()

        is_token_valid = self.context["view"].token_generator.check_token(
            user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise InvalidTokenException()


class TokenObtainPairSerializer(JWTTokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['user'] = UserModelSerializer(self.user).data
        return validated_data