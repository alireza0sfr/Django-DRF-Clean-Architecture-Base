from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    success = False
    detail = ''
    errors = []

    def __init__(self, detail, code, errors=None):
        super().__init__(detail, code)
        if errors is None:
            errors = []
        self.status_code = code
        self.success = False
        self.detail = detail
        self.errors = errors


class EntityNotFoundException(BaseCustomException):
    def __init__(self, message='Entity Not Found!'):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class EntityDeleteRestrictedException(BaseCustomException):
    def __init__(self, message='Entity Deletion Restricted!'):
        super().__init__(message, status.HTTP_409_CONFLICT)


class EntityDeleteProtectedException(BaseCustomException):
    def __init__(self, message='Entity Deletion Protected!'):
        super().__init__(message, status.HTTP_409_CONFLICT)


class CaptchaTokenInvalidException(BaseCustomException):
    def __init__(self, message='Captcha Token is Invalid!'):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class UserBanException(BaseCustomException):
    def __init__(self, message='User is Banned!'):
        super().__init__(message, status.HTTP_403_FORBIDDEN)
