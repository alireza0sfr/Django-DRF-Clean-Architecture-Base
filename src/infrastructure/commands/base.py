from django.db.models.query import Q

from application.dtos.base import BaseDto
from application.interfaces.commands.base import IBaseCommand
from infrastructure.handlers.base import BaseHandler
from infrastructure.validators.validators import Validator, VNotEmpty
from infrastructure.services.dto import DtoService


class BaseCommand(IBaseCommand):
    handler = None
    validator: Validator = Validator
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
        validator: Validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        handler: BaseHandler = self.handler()
        validator.validate({'pk': pk}, validator_roles)
        return handler.get(pk, serialize=serialize)

    def update(self, data, serialize=True):
        dto = self.cast_dto(data)
        handler: BaseHandler = self.handler()
        return handler.update(dto, serialize=serialize)

    def partial_update(self, pk, data, serialize=True):
        handler: BaseHandler = self.handler()
        return handler.partial_update(pk=pk, data=data, serialize=serialize)

    def destroy(self, pk=None):
        validator: Validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        validator.validate({'pk': pk}, validator_roles)
        handler: BaseHandler = self.handler()
        return handler.delete(Q(id=pk))
