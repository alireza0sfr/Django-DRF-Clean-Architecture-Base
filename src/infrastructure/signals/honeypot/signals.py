from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Q
from decouple import config

from domain.apps.identity.models import IPBan
from domain.apps.honeypot.models import LoginAttempt
from domain.enums.identity.enum import BanReasons
from application.dtos.identity.ban import IPBanDto
from infrastructure.handlers.honeypot.honeypot import LoginAttemptHandler
from infrastructure.handlers.identity.ban import IPBanHandler


@receiver(post_save, sender=LoginAttempt)
def ban_ip_if_max_attempts_exceeded(sender, instance, created, **kwargs):
    ip = instance.ip
    login_attempt_handler = LoginAttemptHandler()

    if created and login_attempt_handler.filter(Q(ip=ip)).count() >= config('HONEYPOT_ATTEMPTS', cast=int):
        until = timezone.now() + timezone.timedelta(minutes=config('HONEYPOT_BAN_DURATION_IN_MINUTES', cast=int))
        dto = IPBanDto(ip=ip, reason=BanReasons.HONEYPOT.value, until=until)
        ip_ban_handler = IPBanHandler()
        ip_ban_handler.create(dto)


@receiver(post_delete, sender=IPBan)
def remove_all_related_attempts(sender, instance, **kwargs):
    login_attempt_handler = LoginAttemptHandler()
    login_attempt_handler.delete(Q(ip=instance.ip))
