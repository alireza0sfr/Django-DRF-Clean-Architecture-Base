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

        if not self.repository or not isinstance(self.repository, GenericRepository):
            raise ImproperlyConfigured('Handlers Should define a repository Property!')

        self.raise_serializer_exception = raise_serializer_exception
    
    def get(self, pk: UUID, serialize=True, silent=False) -> QuerySet:
        repository = self.repository()
        result = repository.get(Q(id=pk), silent=silent)
        return self.serializer_class(result).data if serialize else result

    def filter(self, expression: Q, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.filter(expression)
        return self.serializer_class(result, many=True).data if serialize else result

    def get_all(self, serialize=True) -> QuerySet:
        repository = self.repository()
        result = repository.get_all()
        return self.serializer_class(result, many=True).data if serialize else result
    
    def create(self, dto: BaseDto) -> QuerySet:
        repository = self.repository()
        return repository.create(dto)
    
    def bulk_create(self, dtos: list[BaseDto]) -> QuerySet:
        repository = self.repository()
        return repository.bulk_create(dtos)
    
    def delete(self, expression: Q) -> QuerySet:
        repository = self.repository()
        return repository.delete(expression)
    
    def update(self, dto: BaseDto, partial: bool) -> QuerySet:
        repository = self.repository()
        return repository.update(dto, partial=partial)
