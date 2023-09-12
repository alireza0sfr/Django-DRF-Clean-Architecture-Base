from domain.apps.honeypot.models import LoginAttempt
from infrastructure.repositories.generic import GenericRepository
from infrastructure.serializers.honeypot.serializers import LoginAttemptModelSerializer

class LoginAttemptRepository(GenericRepository):
    model = LoginAttempt
    serializer_class = LoginAttemptModelSerializer