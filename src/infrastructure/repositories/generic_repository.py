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

    async def get_async(self, expression: Q) -> QuerySet:
        try:
            return await self.queryset.aget(expression)
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    async def get_by_id_async(self, id: UUID) -> QuerySet:
        return await self.get_async(Q(id=id))

    async def get_all_async(self, expression: Q) -> QuerySet:
        if not expression:
            return await self.queryset
        else:
            return await self.queryset.filter(expression)

    async def create_async(self, entity: Model) -> QuerySet:
        return await entity.asave()

    async def bulk_create_async(self, entities: Model) -> QuerySet:
        return await self.model.objects.abulk_create(entities)

    async def delete_async(self, expression: Q) -> QuerySet:

        try:
            return await self.get_async(expression).adelete()
        except self.model.RestrictedError:
            raise EntityDeleteRestrictedException()
        except self.model.ProtectedError:
            raise EntityDeleteProtectedException()

    async def update_async(self, entity: QuerySet) -> QuerySet:

        try:
            return await entity.aupdate()
        except self.model.DoesNotExist:
            raise EntityNotFoundException()

    async def create_or_update_async(self, entity: QuerySet) -> QuerySet:
        try:
            self.get_by_id_async(id=entity.id)
            return self.update_async(entity)
        except self.model.DoesNotExist:
            return self.create_async(entity)
        except EntityNotFoundException:
            return self.create_async(entity)