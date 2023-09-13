from django.http import HttpRequest
from abc import ABC, abstractmethod

from application.dtos.identity.user import UserDto


class IIPService:

    @abstractmethod
    def get_client_ip(self, request: HttpRequest) -> str:
        pass

    @abstractmethod
    def get_user_ip(self, user: UserDto) -> str:
        pass