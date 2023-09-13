from infrastructure.handlers.base import BaseHandler
from infrastructure.repositories.honeypot.honeypot import LoginAttemptRepository
from infrastructure.serializers.honeypot.serializers import LoginAttemptModelSerializer


class LoginAttemptHandler(BaseHandler):
    repository = LoginAttemptRepository
    serializer_class = LoginAttemptModelSerializer
