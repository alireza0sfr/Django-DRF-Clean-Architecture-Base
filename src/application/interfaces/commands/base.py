from abc import ABC, abstractmethod
from uuid import UUID

from application.dtos.base import BaseDto
from application.interfaces.handlers.base import IBaseHandler


class IBaseCommand(ABC):
    handler: IBaseHandler
    Dto: BaseDto

    @abstractmethod
    def cast_dto(self, data: dict) -> BaseDto:
        pass

    @abstractmethod
    def list(self, serialize: bool):
        pass

    @abstractmethod
    def create(self, data: dict, serialize: bool):
        pass

    @abstractmethod
    def retrieve(self, pk, serialize: bool):
        pass

    @abstractmethod
    def update(self, data: dict, serialize: bool):
        pass

    @abstractmethod
    def partial_update(self, pk: UUID, data: dict, serialize: bool):
        pass

    @abstractmethod
    def destroy(self, pk):
        pass
