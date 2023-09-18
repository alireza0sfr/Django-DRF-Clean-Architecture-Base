from uuid import UUID
from rest_framework.serializers import Serializer
from django.db.models import Q, QuerySet, Model
from django.db.models import ProtectedError, RestrictedError
from django.core.exceptions import ImproperlyConfigured
from typing import Callable

from application.interfaces.repositories.generic import IGenericRepository
from application.dtos.base import BaseDto

from infrastructure.exceptions.exceptions import EntityNotFoundException, EntityDeleteProtectedException, \
    EntityDeleteRestrictedException
from infrastructure.services.dto import DtoService


class GenericRepository(IGenericRepository):
    model: Model = None
    serializer_class: Serializer = None
    queryset: QuerySet = None
    raise_serializer_exception: bool = True

    def __init__(self, raise_serializer_exception: bool = True):

        if not self.model:
            raise ImproperlyConfigured('Repositories Should define a Model Property!')

        if not self.queryset and not isinstance(self.get_queryset, Callable):
            raise ImproperlyConfigured('Repositories Should define either a QuerySet Property or get_queryset Method!')

        if not self.serializer_class and not isinstance(self.serializer_class, Serializer):
            raise ImproperlyConfigured('Repositories Should define either a serializer_class Property!')

        if self.queryset is None:
            self.queryset = self.get_queryset()

        self.raise_serializer_exception = raise_serializer_exception

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def serialize(self, dto: BaseDto | list[BaseDto], many: bool = False) -> Serializer:

        dto_service = DtoService()

        if many:
            data = [dto_service.asdict(value) for count, value in enumerate(dto)]
        else:
            data = dto_service.asdict(dto)

        serializer = self.serializer_class(data=data, many=many)
        serializer.is_valid(raise_exception=self.raise_serializer_exception)
        return serializer

    def get(self, expression: Q) -> QuerySet:
        try:
            return self.queryset.get(expression)
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    def filter(self, expression: Q) -> QuerySet:
        return self.queryset.filter(expression)

    def get_by_pk(self, pk: UUID) -> QuerySet:
        return self.get(Q(pk=pk))
    
    def get_list(self) -> QuerySet:
        return self.queryset

    def get_all(self) -> QuerySet:
        return self.model.objects.all()

    def create(self, dto: BaseDto) -> QuerySet:
        serializer = self.serialize(dto=dto)
        return serializer.save()

    def bulk_create(self, dtos: list[BaseDto]) -> QuerySet:
        serializer = self.serialize(dto=dtos, many=True)
        return serializer.save()

    def delete(self, expression: Q) -> QuerySet:

        try:
            return self.filter(expression).delete()
        except RestrictedError:
            raise EntityDeleteRestrictedException()
        except ProtectedError:
            raise EntityDeleteProtectedException()
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    def update(self, dto: BaseDto) -> QuerySet:
        dto_service = DtoService()
        serializer = self.serializer_class(self.get_by_pk(dto.id), data=dto_service.asdict(dto), partial=False)
        serializer.is_valid(raise_exception=self.raise_serializer_exception)

        try:
            return serializer.save()
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    def partial_update(self, id: UUID, data: dict) -> QuerySet:
        serializer = self.serializer_class(self.get_by_pk(id), data=data, partial=True)
        serializer.is_valid(raise_exception=self.raise_serializer_exception)

        try:
            return serializer.save()
        except self.model.DoesNotExist:
            raise EntityNotFoundException()
