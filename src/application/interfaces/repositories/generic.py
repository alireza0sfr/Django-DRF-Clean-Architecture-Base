from abc import ABC, abstractmethod
from uuid import UUID

from django.db.models import Q, QuerySet, Model
from rest_framework.serializers import Serializer

from application.dtos.base import BaseDto


class IGenericRepository(ABC):

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        pass
    
    @abstractmethod
    def serialize(self, dto: BaseDto) -> Serializer:
        pass

    @abstractmethod
    def get(self, expression: Q, silent: bool, serialize:bool) -> QuerySet:
        pass

    @abstractmethod
    def filter(self, expression: Q, serialize:bool) -> QuerySet:
        pass

    @abstractmethod
    def get_by_pk(self, pk: UUID, silent: bool, serialize: bool) -> QuerySet:
        pass

    @abstractmethod
    def get_all(self, serialize: bool) -> QuerySet:
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
