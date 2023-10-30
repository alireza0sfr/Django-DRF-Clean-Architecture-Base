from infrastructure.responses.responses import (
    BadRequestResponse,
    PermissionDeniedResponse,
    NotFoundResponse,
    ServerErrorResponse,
)


def custom_error_400(request, exception):
    return BadRequestResponse()


def custom_error_403(request, exception):
    return PermissionDeniedResponse()


def custom_error_404(request, exception):
    return NotFoundResponse()


def custom_error_500(request):
    return ServerErrorResponse()
