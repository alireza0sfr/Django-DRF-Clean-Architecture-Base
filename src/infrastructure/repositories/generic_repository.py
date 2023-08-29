from django.db.models import Model, Q, QuerySet
from uuid import UUID

from appplication.interfaces.generic_repository import IGenericRepository
from infrastructure.exceptions.exceptions import EntityNotFoundException, EntityDeleteProtectedException, EntityDeleteRestrictedException


class GenericRepository(IGenericRepository):

    def __init__(self, model: Model):
        self.model = model
        self.queryset = self.get_queryset()

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def get(self, expression: Q) -> QuerySet:
        try:
            return self.queryset.get(expression)
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    def get_by_id(self, id: UUID) -> QuerySet:
        return self.get_sync(Q(id=id))

    def get_all(self, expression: Q) -> QuerySet:
        if not expression:
            return self.queryset
        else:
            return self.queryset.filter(expression)

    def create(self, entity: Model) -> QuerySet:
        return entity.save()

    def bulk_create(self, entities: Model) -> QuerySet:
        return self.model.objects.abulk_create(entities)

    def delete(self, expression: Q) -> QuerySet:

        try:
            return self.get(expression).delete()
        except self.model.RestrictedError:
            raise EntityDeleteRestrictedException()
        except self.model.ProtectedError:
            raise EntityDeleteProtectedException()

    def update(self, entity: QuerySet) -> QuerySet:

        try:
            return entity.update()
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    def create_or_update(self, entity: QuerySet) -> QuerySet:
        try:
            self.get_by_id(id=entity.id)
            return self.update(entity)
        except self.model.DoesNotExist:
            return self.create(entity)
        except EntityNotFoundException:
            return self.create(entity)