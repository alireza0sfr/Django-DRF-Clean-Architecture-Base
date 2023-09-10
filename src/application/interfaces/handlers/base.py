from abc import ABC, abstractmethod
from django.db.models.query import QuerySet, Q
from uuid import UUID
from rest_framework.serializers import Serializer

from application.dtos.base import BaseDto
from application.interfaces.repositories.generic import IGenericRepository


class IBaseHandler(ABC):
    repository: IGenericRepository = None
    serializer_class: Serializer = None
    raise_serializer_exception: bool
    
    @abstractmethod
    def get(self, pk: UUID, serialize=False) -> QuerySet:
        pass
    
    @abstractmethod
    def filter(self, expression: Q, serialize: bool) -> QuerySet:
        pass
    
    @abstractmethod
    def get_all(self, serialize: bool) -> QuerySet:
        pass
    
    @abstractmethod
    def create(self, dto: BaseDto) -> QuerySet:
        pass
    
    @abstractmethod
    def update(self, dto: BaseDto, partial: bool) -> QuerySet:
        pass
    
    @abstractmethod
    def delete(self, pk: UUID) -> QuerySet:
        pass
