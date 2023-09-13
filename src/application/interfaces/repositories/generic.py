from abc import ABC, abstractmethod
from uuid import UUID

from django.db.models import Q, QuerySet
from rest_framework.serializers import Serializer

from application.dtos.base import BaseDto


class IGenericRepository(ABC):

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        pass
    
    @abstractmethod
    def serialize(self, dto:  BaseDto | list[BaseDto], many: bool) -> Serializer:
        pass

    @abstractmethod
    def get(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def filter(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def get_by_pk(self, pk: UUID) -> QuerySet:
        pass

    @abstractmethod
    def get_list(self) -> QuerySet:
        pass

    @abstractmethod
    def get_all(self) -> QuerySet:
        pass

    @abstractmethod
    def create(self, entity: BaseDto) -> QuerySet:
        pass

    @abstractmethod
    def bulk_create(self, entities: list[BaseDto]) -> QuerySet:
        pass

    @abstractmethod
    def delete(self, expression: Q) -> QuerySet:
        pass

    @abstractmethod
    def update(self, dto: BaseDto) -> QuerySet:
        pass

    def partial_update(self, id: UUID, data: dict) -> QuerySet:
        pass