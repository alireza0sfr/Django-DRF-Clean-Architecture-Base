from django.conf import settings
import jwt

from application.interfaces.services.token import ITokenService

class TokenService(ITokenService):

    def decode(self, token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, settings.SIMPLE_JWT.get('algorithm') or 'HS256')
