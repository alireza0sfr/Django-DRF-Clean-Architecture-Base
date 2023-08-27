from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

class TestViewSet(ViewSet):

    def retrieve(self, request):
        return Response(data={'data': 'ok'})