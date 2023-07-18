from uuid import uuid4 as GUID
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(default=GUID, editable=False, unique=True, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
