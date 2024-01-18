from django.db import models
from django.utils.translation import gettext_lazy as _

from domain.base import BaseBanModel


class UserBan(BaseBanModel):
    user = models.ForeignKey('identity.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class IPBan(BaseBanModel):
    ip = models.GenericIPAddressField(unique=True, unpack_ipv4=True)

    def __str__(self):
        return self.ip
