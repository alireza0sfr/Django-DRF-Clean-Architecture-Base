from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JWTTokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer, Serializer, CharField

from domain.apps.accounts.models import User, UserBan, IPBan
from infrastructure.exceptions.exceptions import InvalidTokenException, InvalidIdException, ValidationException, PasswordMissmatchException


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


class IdTokenSerializer(Serializer):
    id = CharField()
    token = CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            user = User.objects.get(pk=self.initial_data.get("uid", ""))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise InvalidIdException()

        is_token_valid = self.context["view"].token_generator.check_token(
            user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise InvalidTokenException()


class PasswordSerializer(Serializer):
    new_password = CharField(style={"input_type": "password"})

    def validate(self, attrs):
        user = getattr(self, "user", None) or self.context["request"].user

        try:
            validate_password(attrs["new_password"], user)
        except django_exceptions.ValidationError as e:
            raise ValidationException(errors=[{"new_password": list(e.messages)}])

        return super().validate(attrs)


class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = CharField(style={"input_type": "password"})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            raise PasswordMissmatchException()


class TokenObtainPairSerializer(JWTTokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['user'] = UserModelSerializer(self.user).data
        return validated_data


class PasswordResetConfirmSerializer(IdTokenSerializer, PasswordSerializer):
    pass


class PasswordResetRetypeConfirmSerializer(IdTokenSerializer, PasswordRetypeSerializer):
    pass
