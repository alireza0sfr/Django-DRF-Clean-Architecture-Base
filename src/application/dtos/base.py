from datetime import datetime
from uuid import UUID

from attrs import define


@define(kw_only=True)
class BaseDto:
    created_date: datetime = ''
    updated_date: datetime = ''
    id: UUID = ''
