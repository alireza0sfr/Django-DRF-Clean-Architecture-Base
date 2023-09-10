from abc import ABC, abstractmethod

from application.interfaces.handlers.base import IBaseHandler
from application.interfaces.validators import IValidator


class IBaseCommand(ABC):
    handler: IBaseHandler
    validator: IValidator

    @abstractmethod
    def list(self, request):
        pass

    @abstractmethod
    def create(self, request):
        pass

    @abstractmethod
    def retrieve(self, request, pk=None):
        pass

    @abstractmethod
    def update(self, request, pk=None):
        pass

    @abstractmethod
    def partial_update(self, request, pk=None):
        pass

    @abstractmethod
    def destroy(self, request, pk=None):
        pass
