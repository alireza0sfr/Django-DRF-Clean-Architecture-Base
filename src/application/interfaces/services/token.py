from abc import ABC, abstractmethod

from domain.apps.identity.models import User

class ITokenService:

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass

    @abstractmethod
    def generate(self, user: User) -> dict:
        pass