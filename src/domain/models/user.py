from attrs import define
from django.utils import timezone

from appplication.dtos.base import BaseDto


@define
class UserDto(BaseDto):
    username: str
    password: str
    email: str

    last_login: timezone
    date_joined: timezone

    is_active: bool
    is_verified: bool
    is_superuser: bool
    is_staff: bool
    is_anonymous: bool
