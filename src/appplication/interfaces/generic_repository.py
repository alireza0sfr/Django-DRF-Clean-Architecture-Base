from django.db.models import Model, Q, QuerySet
from uuid import UUID
from abc import ABC, abstractmethod


class IGenericRepository(ABC):

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        pass

    @abstractmethod
    async def get_async(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    async def get_by_id_async(self, id: UUID) -> QuerySet:
        pass

    @abstractmethod
    async def get_all_async(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    async def create_async(self, entity: Model) -> QuerySet:
        pass

    @abstractmethod
    async def bulk_create_async(self, entities: Model) -> QuerySet:
        pass

    @abstractmethod
    async def delete_async(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    async def update_async(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    async def create_or_update_async(self, entity: QuerySet) -> QuerySet:
        pass