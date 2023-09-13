from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from domain.apps.identity.managers import UserManager
from domain.base import BaseModel, BaseBanModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True, unique=True, error_messages={
        "unique": _("A user with that email already exists."),
    }, )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_used_ip = models.GenericIPAddressField(_("last used ip"), blank=True, null=True)

    objects = UserManager()

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class UserBan(BaseBanModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class IPBan(BaseBanModel):
    ip = models.GenericIPAddressField(unique=True, unpack_ipv4=True)

    def __str__(self):
        return self.ip
