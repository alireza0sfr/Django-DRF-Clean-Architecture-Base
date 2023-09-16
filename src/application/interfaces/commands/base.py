from abc import ABC, abstractmethod

from application.dtos.base import BaseDto
from application.interfaces.handlers.base import IBaseHandler
from application.interfaces.validators import IValidator


class IBaseCommand(ABC):
    handler: IBaseHandler
    validator: IValidator
    Dto: BaseDto

    @abstractmethod
    def cast_dto(self, data: dict) -> BaseDto:
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, data: dict):
        pass

    @abstractmethod
    def retrieve(self, pk):
        pass

    @abstractmethod
    def update(self, data: dict):
        pass

    @abstractmethod
    def partial_update(self, data: dict):
        pass

    @abstractmethod
    def destroy(self, pk):
        pass
