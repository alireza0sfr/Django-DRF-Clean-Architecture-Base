from django.db.models import Model, Q, QuerySet
from uuid import UUID
from abc import ABC, abstractmethod


class IGenericRepository(ABC):

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        pass

    @abstractmethod
    def get(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> QuerySet:
        pass

    @abstractmethod
    def get_all(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def create(self, entity: Model) -> QuerySet:
        pass

    @abstractmethod
    def bulk_create(self, entities: Model) -> QuerySet:
        pass

    @abstractmethod
    def delete(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def update(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def create_or_update(self, entity: QuerySet) -> QuerySet:
        pass