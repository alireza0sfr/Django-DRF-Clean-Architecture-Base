from django.db.models.query import Q
from uuid import UUID

from application.dtos.base import BaseDto
from application.interfaces.commands.base import IBaseCommand
from infrastructure.handlers.base import BaseHandler
from infrastructure.services.dto import DtoService


class BaseCommand(IBaseCommand):
    handler = None
    Dto: BaseDto

    def __init__(self):

        if not self.handler or not issubclass(self.handler, BaseHandler):
            raise NotImplementedError('BaseCommand must have a handler attribute and it must be a subclass of '
                                      'BaseHandler')

    def cast_dto(self, data: dict) -> BaseDto:
        dto_service = DtoService()
        return dto_service.cast(data, self.Dto)

    def list(self, serialize=True):
        handler: BaseHandler = self.handler()
        return handler.get_all(serialize=serialize)

    def create(self, data, serialize=True):
        handler: BaseHandler = self.handler()
        dto = self.cast_dto(data)
        return handler.create(dto, serialize=serialize)

    def retrieve(self, pk=None, serialize=True):
        handler: BaseHandler = self.handler()
        return handler.get(pk=pk, serialize=serialize)

    def update(self, data, serialize=True):
        dto = self.cast_dto(data)
        handler: BaseHandler = self.handler()
        return handler.update(dto, serialize=serialize)

    def partial_update(self, pk: UUID, data: dict, serialize=True):
        handler: BaseHandler = self.handler()
        return handler.partial_update(pk=pk, data=data, serialize=serialize)

    def destroy(self, pk=None):
        handler: BaseHandler = self.handler()
        return handler.delete(Q(id=pk))
