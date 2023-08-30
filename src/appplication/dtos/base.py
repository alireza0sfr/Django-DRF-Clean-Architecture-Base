from uuid import uuid4 as GUID

from attrs import define
from django.utils import timezone


@define(frozen=True)
class BaseDto:
    created_date: timezone
    updated_date: timezone
    id: GUID
