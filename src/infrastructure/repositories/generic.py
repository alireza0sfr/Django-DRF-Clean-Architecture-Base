from uuid import UUID

from django.db.models import Q, QuerySet, Model

from application.interfaces.repositories.generic import IGenericRepository
from infrastructure.exceptions.exceptions import EntityNotFoundException, EntityDeleteProtectedException, \
    EntityDeleteRestrictedException
from infrastructure.mapper.mapper import Mapper


class GenericRepository(IGenericRepository):
    model = None
    mapper = Mapper()
    queryset = None

    def __init__(self):
        if self.queryset is None:
            self.queryset = self.get_queryset()

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def get(self, expression: Q, silent=False) -> QuerySet | None:
        try:
            return self.queryset.get(expression)
        except self.model.DoesNotExist:
            if silent:
                return None
            raise EntityNotFoundException()

    def filter(self, expression: Q) -> QuerySet:
        return self.queryset.filter(expression)

    def get_by_id(self, id: UUID, silent=False) -> QuerySet | None:
        return self.get(Q(id=id), silent)

    def get_all(self, expression: Q) -> QuerySet:
        if not expression:
            return self.queryset
        else:
            return self.queryset.filter(expression)

    def create(self, entity: Model) -> QuerySet:
        return entity.save(force_insert=True)

    def bulk_create(self, entities: list[Model]) -> QuerySet:
        return self.model.objects.abulk_create(entities)

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

    def create_or_update(self, entity: Model) -> QuerySet:
        try:
            self.get_by_id(id=entity.pk)
            return self.update(entity)
        except self.model.DoesNotExist:
            return self.create(entity)
        except EntityNotFoundException:
            return self.create(entity)
