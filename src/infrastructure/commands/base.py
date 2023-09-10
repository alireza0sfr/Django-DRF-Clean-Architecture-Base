from django.db.models.query import Q

from application.interfaces.commands.base import IBaseCommand
from infrastructure.handlers.base import BaseHandler
from infrastructure.validators.validators import Validator, VNotEmpty


class BaseCommand(IBaseCommand):
    handler = None
    validator = Validator

    def __init__(self):

        if not self.handler or issubclass(self.handler, BaseHandler):
            raise NotImplementedError('BaseCommand must have a handler attribute and it must be a subclass of '
                                      'BaseHandler')

    def list(self, request):
        return self.handler.get_all()

    def create(self, request):
        return self.handler.create(request.data)

    def retrieve(self, request, pk=None):
        validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        validator.validate({'pk': pk}, validator_roles)
        return self.handler.get(pk)

    def update(self, request, pk=None):
        validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        validator.validate({'pk': pk}, validator_roles)
        return self.handler.update(pk, request.data, partial=False)

    def partial_update(self, request, pk=None):
        validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        validator.validate({'pk': pk}, validator_roles)
        return self.handler.update(pk, request.data, partial=True)

    def destroy(self, request, pk=None):
        validator = self.validator()
        validator_roles = {
            'pk': [VNotEmpty]
        }
        validator.validate({'pk': pk}, validator_roles)
        return self.handler.delete(Q(id=pk))
