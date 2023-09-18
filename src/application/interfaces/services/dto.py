from abc import ABC, abstractmethod

from application.dtos.base import BaseDto


class IDtoService(ABC):

    @abstractmethod
    def asdict(self, dto) -> dict:
        pass

    @abstractmethod
    def cast(self, data: dict, dto: BaseDto) -> BaseDto:
        pass
