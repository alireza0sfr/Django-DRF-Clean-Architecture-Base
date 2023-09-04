import attrs

from application.interfaces.mapper import IMapper


class Mapper(IMapper):

    @classmethod
    def map(cls, dto, model):
        model_fields = model._meta.fields

        model_attributes = {}
        dto_dict = attrs.asdict(dto)

        for field in model_fields:
            field_name = field.name
            if field_name in dto_dict:
                model_attributes[field_name] = dto_dict[field_name]

        return model(**model_attributes)
