from datetime import datetime

from attrs import define

from application.dtos.accounts.user import UserDto


@define
class BaseBanDto:
    until: datetime
    reason: str
    description: str


@define
class UserBanDto(BaseBanDto):
    user: UserDto


class IPBanDto(BaseBanDto):
    ip: str
