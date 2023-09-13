from abc import ABC, abstractmethod


class ITokenService:

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass