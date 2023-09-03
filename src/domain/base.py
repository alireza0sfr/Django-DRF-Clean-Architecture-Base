from uuid import uuid4 as GUID

from django.db import models

from .enums.accounts.enum import BanReasons


class BaseModel(models.Model):
    id = models.UUIDField(default=GUID, editable=False, unique=True, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_date',)


class BaseBanModel(BaseModel):
    until = models.DateTimeField()
    reason = models.CharField(default=BanReasons.ABUSIVE.value, choices=BanReasons.choices, max_length=20)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
