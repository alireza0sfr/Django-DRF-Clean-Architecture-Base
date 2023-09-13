from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from domain.apps.identity.models import User
from application.interfaces.services.token import ITokenService
from infrastructure.serializers.identity.serializers import UserModelSerializer

class TokenService(ITokenService):

    def decode(self, token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, settings.SIMPLE_JWT.get('algorithm') or 'HS256')

    def generate(self, user: User) -> dict:
        refresh = RefreshToken.for_user(user)

        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
            'user': UserModelSerializer(user).data
        }