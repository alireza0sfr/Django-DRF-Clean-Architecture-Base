from uuid import UUID
from rest_framework.serializers import Serializer
from django.db.models import Q, QuerySet, Model
from django.core.exceptions import ImproperlyConfigured

from application.interfaces.repositories.generic import IGenericRepository
from application.dtos.base import BaseDto

from infrastructure.exceptions.exceptions import EntityNotFoundException, EntityDeleteProtectedException, \
    EntityDeleteRestrictedException


class GenericRepository(IGenericRepository):
    model: Model = None
    serializer_class: Serializer = None
    queryset: QuerySet = None
    raise_serializer_exception: bool = True

    def __init__(self, raise_serializer_exception: bool=True):

        if not self.model:
            raise ImproperlyConfigured('Repositories Should define a Model Property!')

        if not self.queryset or type(self.get_queryset()) != 'function':
            raise ImproperlyConfigured('Repositories Should define either a QuerySet Property or get_queryset Method!')

        if not self.serializer_class or not isinstance(self.serializer_class, Serializer):
            raise ImproperlyConfigured('Repositories Should define either a serializer_class Property!')

        if self.queryset is None:
            self.queryset = self.get_queryset()

        self.raise_serializer_exception = raise_serializer_exception

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def serialize(self, dto: BaseDto | list[BaseDto], many: bool=False) -> Serializer:
        serializer = self.serializer_class(data=dto, many=many)
        serializer.is_valid(raise_exception=self.raise_serializer_exception)
        return serializer

    def get(self, expression: Q, silent=False, serialize=False) -> QuerySet | None:
        try:
            result = self.queryset.get(expression)
            return result if not serialize else self.serializer_class(result).data
        except self.model.DoesNotExist:
            if silent:
                return None
            raise EntityNotFoundException()

    def filter(self, expression: Q, serialize=False) -> QuerySet:
        result = self.queryset.filter(expression)
        return result if not serialize else self.serializer_class(result, many=True).data

    def get_by_id(self, id: UUID, silent=False, serialize=False) -> QuerySet | None:
        return self.get(Q(id=id), silent, serialize)

    def get_all(self, serialize=False) -> QuerySet:
        result = self.queryset
        return result if not serialize else self.serializer_class(result, many=True)

    def create(self, dto: BaseDto) -> QuerySet:
        serializer = self.serialize(dto=dto)
        return serializer.save()

    def bulk_create(self, dtos: list[BaseDto]) -> QuerySet:
        serializer = self.serialize(dto=dtos, many=True)
        return serializer.save()

    def delete(self, expression: Q) -> QuerySet:

        try:
            return self.get(expression).delete()
        except self.model.RestrictedError:
            raise EntityDeleteRestrictedException()
        except self.model.ProtectedError:
            raise EntityDeleteProtectedException()

    def update(self, entity: Model) -> QuerySet:

        try:
            return entity.save(force_update=True)
        except self.model.DoesNotExist:
            raise EntityNotFoundException()