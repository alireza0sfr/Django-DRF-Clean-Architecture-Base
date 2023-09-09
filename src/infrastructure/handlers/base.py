from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet, Q
from rest_framework.serializers import Serializer

from attr import asdict
from uuid import UUID

from application.dtos.base import BaseDto
from application.interfaces.repositories.generic import IGenericRepository
from application.interfaces.handlers.base import IBaseHandler


class BaseHandler(IBaseHandler):
    serializer_class: Serializer = None
    repository: IGenericRepository = None
    raise_serializer_exception: bool = True

    def __init__(self, raise_serializer_exception: bool = True):
        if not self.serializer_class:
            raise ImproperlyConfigured('Handlers Should define a serializer_class Property!')

        if not self.repository:
            raise ImproperlyConfigured('Handlers Should define a repository Property!')

        self.raise_serializer_exception = raise_serializer_exception
    
    def get(self, pk: UUID, serialize=True, silent=False) -> QuerySet:
        result = self.repository.get(Q(id=pk), silent=silent)
        return self.serializer_class(result).data if serialize else result

    def filter(self, expression: Q, serialize=True) -> QuerySet:
        result = self.repository.filter(expression)
        return self.serializer_class(result, many=True).data if serialize else result

    def list(self, serialize=True) -> QuerySet:
        result = self.repository.get_all()
        return self.serializer_class(result, many=True).data if serialize else result
    
    def create(self, dto: BaseDto) -> QuerySet:
        return self.repository.create(dto)
    
    def bulk_create(self, dtos: list[BaseDto]) -> QuerySet:
        return self.repository.bulk_create(dtos)
    
    def delete(self, expression: Q) -> QuerySet:
        return self.repository.delete(expression)
    
    def update(self, dto: BaseDto, partial: bool) -> QuerySet:
        return self.repository.update(dto, partial=partial)