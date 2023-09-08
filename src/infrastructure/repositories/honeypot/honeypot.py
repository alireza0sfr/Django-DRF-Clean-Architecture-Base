from domain.apps.honeypot.models import Honeypot
from infrastructure.repositories.generic import GenericRepository
from infrastructure.serializers.honeypot.serializers import HoneypotModelSerializer

class HoneypotRepository(GenericRepository):
    model = Honeypot
    serializer_class = HoneypotModelSerializer