from rest_framework.views import exception_handler
from infrastructure.exceptions.exceptions import BaseCustomException
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(exc, BaseCustomException):
        response.data["errors"] = exc.errors
        response.data["key"] = exc.key

    # Handle Python exceptions
    elif isinstance(exc, Exception) and not isinstance(exc, APIException):
        response = Response(
            data={
                "errors": exc.args,
                "message": "Internal Server Error!",
                "key": "internal_server_error",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
