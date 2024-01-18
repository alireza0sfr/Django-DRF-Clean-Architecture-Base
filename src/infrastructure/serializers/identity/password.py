from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework.serializers import Serializer, CharField

from infrastructure.exceptions.exceptions import ValidationException, PasswordMissmatchException

from .token import IdTokenSerializer

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



class PasswordResetConfirmSerializer(IdTokenSerializer, PasswordSerializer):
    pass


class PasswordResetRetypeConfirmSerializer(IdTokenSerializer, PasswordRetypeSerializer):
    pass