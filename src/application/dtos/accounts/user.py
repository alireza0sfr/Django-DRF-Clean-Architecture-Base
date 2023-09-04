from datetime import datetime

from attrs import define


@define
class UserDto:
    username: str
    password: str
    email: str

    last_login: datetime
    date_joined: datetime
    last_used_ip: str

    is_active: bool
    is_verified: bool
    is_superuser: bool
    is_staff: bool
    is_hidden: bool
