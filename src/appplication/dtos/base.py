from uuid import UUID
from attrs import define
from datetime import datetime

@define
class BaseDto:
    created_date: datetime
    updated_date: datetime
    id: UUID
