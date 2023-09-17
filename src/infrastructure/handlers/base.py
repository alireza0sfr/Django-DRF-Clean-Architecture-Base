from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet, Q

from uuid import UUID

from application.dtos.base import BaseDto
from application.interfaces.handlers.base import IBaseHandler

from infrastructure.repositories.generic import GenericRepository


class BaseHandler(IBaseHandler):
    serializer_class = None
    repository = None
    raise_serializer_exception = True

    def __init__(self, raise_serializer_exception: bool = True):
        if not self.serializer_class:
            raise ImproperlyConfigured('Handlers Should define a serializer_class Property!')

        if not self.repository or not issubclass(self.repository, GenericRepository):
            raise ImproperlyConfigured('Handlers Should define a repository Property!')

        self.raise_serializer_exception = raise_serializer_exception
    
    def get(self, expression: Q, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.get(expression=expression)
        return self.serializer_class(result).data if serialize else result
    
    def get_by_pk(self, pk: UUID, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.get_by_pk(pk=pk)
        return self.serializer_class(result).data if serialize else result

    def filter(self, expression: Q, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.filter(expression)
        return self.serializer_class(result, many=True).data if serialize else result

    def get_all(self, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.get_all()
        return self.serializer_class(result, many=True).data if serialize else result
    
    def create(self, dto: BaseDto, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.create(dto)
        return self.serializer_class(result).data if serialize else result
    
    def bulk_create(self, dtos: list[BaseDto], serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.bulk_create(dtos)
        return self.serializer_class(result, many=True).data if serialize else result
    
    def delete(self, expression: Q) -> QuerySet:
        repository = self.repository()
        result = repository.delete(expression)
        return result
    
    def update(self, dto: BaseDto, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.update(dto)
        return self.serializer_class(result).data if serialize else result

    def partial_update(self, pk: UUID, data: dict = None, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.partial_update(pk, data)
        return self.serializer_class(result).data if serialize else result
