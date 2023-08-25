from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    success = False
    detail = ''
    erros = []

    def __init__(self, detail, code, errors):
        super().__init__(detail, code)
        self.status_code = code
        self.success = False
        self.detail = detail
        self.errors = errors


class EntityNotFoundException(BaseCustomException):
  def __init__(self, message):
    super().__init__(message, status.HTTP_404_NOT_FOUND)


class EntityDeleteRestrictedException(BaseCustomException):
  def __init__(self, message):
    super().__init__(message, status.HTTP_409_CONFLICT)


class EntityDeleteProtectedException(BaseCustomException):
  def __init__(self, message):
    super().__init__(message, status.HTTP_409_CONFLICT)