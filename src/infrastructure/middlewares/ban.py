from django.db.models import Q
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from infrastructure.exceptions.exceptions import UserBanException
from infrastructure.repositories.identity.ban import UserBanRepository, IPBanRepository
from infrastructure.services.ip import IPService


class BanMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        assert hasattr(request, "session"), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        ip = IPService().get_client_ip(request)
        user = request.user

        if user.is_authenticated:
            user.last_used_ip = ip
            user.save()

            user_ban_repository = UserBanRepository()
            user_ban = user_ban_repository.filter(Q(user=user, until__gt=timezone.now()))

            if user_ban.exists():
                raise UserBanException(errors=[
                    {
                        'until': user_ban[0].until,
                        'reason': user_ban[0].reason,
                        'description': user_ban[0].description
                    }
                ])

        ip_ban_repository = IPBanRepository()
        ip_ban = ip_ban_repository.filter(Q(ip=ip, until__gt=timezone.now()))
        if ip_ban.exists():
            raise UserBanException(errors=[
                {
                    'until': ip_ban[0].until,
                    'reason': ip_ban[0].reason,
                    'description': ip_ban[0].description
                }
            ])
