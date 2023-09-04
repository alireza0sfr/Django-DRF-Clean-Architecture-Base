from abc import ABC, abstractmethod
from uuid import UUID

from django.db.models import Q, QuerySet, Model


class IGenericRepository(ABC):

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        pass

    @abstractmethod
    def get(self, expression: Q, silent=False) -> QuerySet:
        pass

    @abstractmethod
    def filter(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID, silent=False) -> QuerySet:
        pass

    @abstractmethod
    def get_all(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def create(self, entity: Model) -> QuerySet:
        pass

    @abstractmethod
    def bulk_create(self, entities: list[Model]) -> QuerySet:
        pass

    @abstractmethod
    def delete(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def update(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def create_or_update(self, entity: Model) -> QuerySet:
        pass
