from datetime import datetime

from attrs import define

from application.dtos.base import BaseDto

@define
class UserDto(BaseDto):
    username: str
    email: str

    is_active: bool = True
    is_verified: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    is_hidden: bool = False

    password: str = ''
    last_login: datetime = ''
    date_joined: datetime = ''
    last_used_ip: str = ''
