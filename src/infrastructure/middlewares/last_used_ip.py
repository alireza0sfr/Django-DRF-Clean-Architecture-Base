from infrastructure.services.ip import IP


class LastUsedIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            ip = IP()
            request.user.last_used_ip = ip.get_client_ip(request)
            request.user.save()

        return response
