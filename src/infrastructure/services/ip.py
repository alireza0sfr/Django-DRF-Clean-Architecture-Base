from django.http import HttpRequest

from application.dtos.identity.user import UserDto
from application.interfaces.services.ip import IIPService

class IPService(IIPService):

    def get_client_ip(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def get_user_ip(self, user: UserDto) -> str:
        return user.last_used_ip