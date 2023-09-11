from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Q
from decouple import config

from domain.apps.identity.models import IPBan
from domain.apps.honeypot.models import Honeypot
from domain.enums.identity.enum import BanReasons
from application.dtos.identity.ban import IPBanDto
from infrastructure.repositories.honeypot.honeypot import HoneypotRepository
from infrastructure.repositories.identity.ban import IPBanRepository


@receiver(post_save, sender=Honeypot)
def ban_ip_if_max_attempts_exceeded(sender, instance, created, **kwargs):
    ip = instance.ip
    honeypot_repository = HoneypotRepository()

    if created and honeypot_repository.filter(Q(ip=ip)).count() >= config('HONEYPOT_ATTEMPTS', cast=int):
        until = timezone.now() + timezone.timedelta(minutes=config('HONEYPOT_BAN_DURATION_IN_MINUTES', cast=int))
        dto = IPBanDto(ip=ip, reason=BanReasons.HONEYPOT.value, until=until)
        ip_ban_repository = IPBanRepository()
        ip_ban_repository.create(dto)


@receiver(post_delete, sender=IPBan)
def remove_all_related_attempts(sender, instance, **kwargs):
    honeypot_repository = HoneypotRepository()
    honeypot_repository.delete(Q(ip=instance.ip))
