from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    success = False
    message = ''
    erros = []

    def __init__(self, message, code, errors):
        super().__init__(message, code)
        self.status_code = code
        self.success = False
        self.message = message
        self.errors = errors


class EntityNotFoundException(BaseCustomException):
  def __init__(self, message):
    super().__init__(message, status.HTTP_404_NOT_FOUND)