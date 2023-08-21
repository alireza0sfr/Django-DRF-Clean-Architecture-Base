from django.db.models import Model, Q, QuerySet
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID

from appplication.interfaces.generic_repository import IGenericRepository


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
            raise ObjectDoesNotExist('Entity Not Found!')

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
        return await self.get_async(expression).adelete()

    async def update_async(self, expression: Q) -> QuerySet:
        return await self.get_async(expression).aupdate()

    async def create_or_update_async(self, entity: QuerySet) -> QuerySet:
        if self.get_by_id_async(entity.id):
            return self.update_async(entity)
        else:
            return self.create_async(entity)
