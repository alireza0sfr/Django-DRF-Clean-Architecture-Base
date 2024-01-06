import json

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import status


class BaseJsonResponse(JsonResponse):
    def __init__(self, data, message, code, key, **kwargs):
        self.data = data
        self.message = message
        self.code = code
        self.key = key

        super().__init__(data=self.prepare_data(), **kwargs, status=self.code)

    def prepare_data(self):
        return {
            "success": False,
            "key": self.key,
            "code": self.code,
            "message": self.message,
            "data": self.data,
        }


class UserBanResponse(BaseJsonResponse):
    def __init__(self, data=None, message="User is Banned!", key="user_is_banned"):
        super().__init__(
            data=data, message=message, code=status.HTTP_403_FORBIDDEN, key=key
        )


class BadRequestResponse(BaseJsonResponse):
    def __init__(self, data=None, message="Bad Request!", key="bad_request"):
        super().__init__(
            data=data, message=message, code=status.HTTP_400_BAD_REQUEST, key=key
        )


class PermissionDeniedResponse(BaseJsonResponse):
    def __init__(
        self, data=None, message="Permission Denied!", key="permission_denied"
    ):
        super().__init__(
            data=data, message=message, code=status.HTTP_403_FORBIDDEN, key=key
        )


class NotFoundResponse(BaseJsonResponse):
    def __init__(self, data=None, message="Not Found!", key="not_found"):
        super().__init__(
            data=data, message=message, code=status.HTTP_404_NOT_FOUND, key=key
        )


class ServerErrorResponse(BaseJsonResponse):
    def __init__(self, data=None, message="Server Error!", key="server_error"):
        super().__init__(
            data=data,
            message=message,
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            key=key,
        )
