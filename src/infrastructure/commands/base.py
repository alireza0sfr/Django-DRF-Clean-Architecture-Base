from django.db.models.query import Q, QuerySet
from uuid import UUID

from rest_framework.views import APIView
from django.http.request import HttpRequest

from application.dtos.base import BaseDto
from application.interfaces.commands.base import IBaseCommand
from infrastructure.handlers.base import BaseHandler
from infrastructure.services.dto import DtoService


class BaseCommand(IBaseCommand):
    handler: BaseHandler = None
    Dto: BaseDto
    view: APIView
    request: HttpRequest

    def __init__(self, view, request):

        if not self.handler or not issubclass(self.handler, BaseHandler):
            raise NotImplementedError(
                "BaseCommand must have a handler attribute and it must be a subclass of "
                "BaseHandler"
            )

        if not view or not isinstance(view, APIView):
            raise NotImplementedError(
                "BaseCommand must have a view attribute and it must be a subclass of "
                "Django View"
            )

        if not request:
            raise NotImplementedError("BaseCommand must have a request attribute")

        self.view = view
        self.request = request

    def cast_dto(self, data: dict) -> BaseDto:
        dto_service = DtoService()
        return dto_service.cast(data, self.Dto)

    def check_object_permissions(self, obj: QuerySet):
        self.view.check_object_permissions(self.request, obj)

    def list(self, serialize=True):
        handler: BaseHandler = self.handler()
        result = handler.get_list(serialize=False)

        self.check_object_permissions(result)
        return handler.serializer_class(result, many=True).data if serialize else result

    def create(self, data, serialize=True):
        handler: BaseHandler = self.handler()
        dto = self.cast_dto(data)
        return handler.create(dto, serialize=serialize)

    def retrieve(self, pk=None, serialize=True):
        handler: BaseHandler = self.handler()
        result = handler.get_by_pk(pk=pk, serialize=False)

        self.check_object_permissions(result)
        return handler.serializer_class(result).data if serialize else result

    def update(self, data, serialize=True):
        dto = self.cast_dto(data)
        handler: BaseHandler = self.handler()
        result = handler.update(dto, serialize=False)

        self.check_object_permissions(result)
        return handler.serializer_class(result).data if serialize else result

    def partial_update(self, pk: UUID, data: dict, serialize=True):
        handler: BaseHandler = self.handler()
        result = handler.partial_update(pk=pk, data=data, serialize=False)

        self.check_object_permissions(result)
        return handler.serializer_class(result).data if serialize else result

    def destroy(self, pk=None):
        handler: BaseHandler = self.handler()
        return handler.delete(Q(id=pk))
