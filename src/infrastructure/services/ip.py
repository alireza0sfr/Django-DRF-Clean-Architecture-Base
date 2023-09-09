from django.http import HttpRequest

from application.dtos.accounts.user import UserDto


class IPService:
    @staticmethod
    def get_client_ip(request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_user_ip(user: UserDto):
        return user.last_used_ip
