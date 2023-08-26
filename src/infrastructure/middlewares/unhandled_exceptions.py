from rest_framework.exceptions import APIException
from infrastructure.exceptions.exceptions import BaseCustomException
from rest_framework.response import Response


class UnhandledExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except APIException as api_exception:
            custom_exception = BaseCustomException(
                detail=str(api_exception.detail),
                code=api_exception.status_code,
                errors=api_exception.get_codes(),
            )
            return Response(custom_exception)
