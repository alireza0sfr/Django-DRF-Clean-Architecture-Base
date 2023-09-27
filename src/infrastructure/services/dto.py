from attr import asdict
from cattrs import structure
from django.db.models import Model

from application.dtos.base import BaseDto
from application.interfaces.services.dto import IDtoService
from infrastructure.exceptions.exceptions import CastDtoException


class DtoService(IDtoService):

    def asdict(self, dto) -> dict:
        return asdict(dto)

    def cast(self, data: dict, dto: BaseDto):
        try:
            return structure(data, dto)
        except Exception as e:
            errors = []
            for index, x in enumerate(e.exceptions):
                errors.append({index: x.__notes__[0]})
            raise CastDtoException(errors=errors, message=e.message)

    def cast_from_model(self, model: Model, dto):
        return self.cast(model.__dict__, dto)