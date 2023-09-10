from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    success = False
    errors = None

    def __init__(self, detail, code, errors=None):
        super().__init__(detail, code)
        self.status_code = code
        self.success = False
        self.errors = errors


class EntityNotFoundException(BaseCustomException):
    def __init__(self, message='Entity Not Found!', errors=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, errors)


class EntityDeleteRestrictedException(BaseCustomException):
    def __init__(self, message='Entity Deletion Restricted!', errors=None):
        super().__init__(message, status.HTTP_409_CONFLICT, errors)


class EntityDeleteProtectedException(BaseCustomException):
    def __init__(self, message='Entity Deletion Protected!', errors=None):
        super().__init__(message, status.HTTP_409_CONFLICT, errors)


class CaptchaTokenInvalidException(BaseCustomException):
    def __init__(self, message='Captcha Token is Invalid!', errors=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, errors)


class UserBanException(BaseCustomException):
    def __init__(self, message='User is Banned!', errors=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, errors)


class ValidationException(BaseCustomException):
    def __init__(self, message='Validation Error!', errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, errors)


class InvalidTokenException(BaseCustomException):
    def __init__(self, message='Token is Invalid!', errors=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, errors)


class InvalidIdException(BaseCustomException):
    def __init__(self, message='id is Invalid!', errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, errors)


class PasswordMissmatchException(BaseCustomException):
    def __init__(self, message='Password Missmatch!', errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, errors)