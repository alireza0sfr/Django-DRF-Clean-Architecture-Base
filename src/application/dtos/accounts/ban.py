from datetime import datetime

from attrs import define

from application.dtos.accounts.user import UserDto
from application.dtos.base import BaseDto

@define(kw_only=True)
class BaseBanDto(BaseDto):
    until: datetime
    reason: str
    description: str = ''


@define
class UserBanDto(BaseBanDto):
    user: UserDto


@define
class IPBanDto(BaseBanDto):
    ip: str
