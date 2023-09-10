from enum import Enum

from application.interfaces.validators import IValidator
from infrastructure.exceptions.exceptions import ValidationException


class Validator:
    @staticmethod
    def validate(data, validators, message_generator=None):

        errors = []

        for key, value in validators.items():
            prop = data.get(key)

            for index, v in enumerate(value):

                validator = v if isinstance(v, IValidator) else v.value()
                validated = validator.validate(prop)

                if not validated:
                    errors.append({
                        'message': message_generator(key) if message_generator else validator.message_generator(key),
                        'value': prop,
                    })

        if len(errors) > 0:
            raise ValidationException(errors)


class VNotEmpty(IValidator):

    @staticmethod
    def validate(value):
        return not is_empty(value)

    @staticmethod
    def message_generator(value):
        return f'{value} is required!'


class VCustom(IValidator):

    def __init__(self, validator, mgenerator) -> None:
        self.validator = validator
        self.mgenerator = mgenerator

    def validate(self, value):
        return self.validator(value)

    def message_generator(self, value):
        return self.mgenerator(value)


class VEmail(IValidator):

    def validate(self, value):
        import re

        regex = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
        return bool(re.match(regex, value))

    def message_generator(self, value):
        return f'{value} is not a valid email!'


class TValidators(Enum):
    NotEmpty = VNotEmpty
    Custom = VCustom
    Email = VEmail


def is_empty(value):
    if (value is None or
            value == 0 or
            value == 0.0 or
            value == '0.0000' or
            value == '0' or
            value == '00000000-0000-0000-0000-000000000000' or
            str(value).strip() == '' or
            (isinstance(value, list) and len(value) == 0)):
        return True

    return False
