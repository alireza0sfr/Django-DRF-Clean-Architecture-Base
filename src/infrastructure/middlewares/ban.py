from django.utils.deprecation import MiddlewareMixin

from domain.apps.accounts.models import UserBan, IPBan
from infrastructure.exceptions.exceptions import UserBanException
from infrastructure.services.ip import IP


class BanMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, "session"), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        ip = IP().get_client_ip(request)
        user = request.user

        if request.user.is_authenticated:
            user.last_used_ip = ip
            user.save()

            if UserBan.objects.filter(user=user).exists():
                raise UserBanException()

        if IPBan.objects.filter(ip=ip).exists():
            raise UserBanException()
