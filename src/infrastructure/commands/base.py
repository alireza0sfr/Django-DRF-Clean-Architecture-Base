from django.db.models.query import Q
from cattrs import structure

from application.dtos.base import BaseDto
from application.interfaces.commands.base import IBaseCommand
from infrastructure.handlers.base import BaseHandler
from infrastructure.validators.validators import Validator, VNotEmpty


class BaseCommand(IBaseCommand):
    handler: BaseHandler = None
    validator: Validator = Validator
    Dto = BaseDto

    def __init__(self):

        if not self.handler or not issubclass(self.handler, BaseHandler):
            raise NotImplementedError('BaseCommand must have a handler attribute and it must be a subclass of '
                                      'BaseHandler')

    def list(self, request):
        handler: BaseHandler = self.handler()
        return handler.get_all()

    def create(self, request):
        handler: BaseHandler = self.handler()
        dto = structure(request.data, self.Dto)
        return handler.create(dto)

    def retrieve(self, request, pk=None):
        validator: Validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        handler: BaseHandler = self.handler()
        validator.validate({'pk': pk}, validator_roles)
        return handler.get(pk)

    def update(self, request, pk=None):
        validator: Validator = self.validator()
        validator_roles = {
            'id': [VNotEmpty]
        }
        dto = structure(request.data, self.Dto)
        validator.validate(dto, validator_roles)
        handler: BaseHandler = self.handler()
        return handler.update(dto, partial=False)

    def partial_update(self, request, pk=None):
        validator: Validator = self.validator()
        validator_roles = {
            'id': [VNotEmpty]
        }
        dto = structure(request.data, self.Dto)
        validator.validate(dto, validator_roles)
        handler: BaseHandler = self.handler()
        return handler.update(dto, partial=True)

    def destroy(self, request, pk=None):
        validator: Validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        validator.validate({'pk': pk}, validator_roles)
        handler: BaseHandler = self.handler()
        return handler.delete(Q(id=pk))
