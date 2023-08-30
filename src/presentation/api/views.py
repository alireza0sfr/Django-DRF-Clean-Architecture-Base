from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class TestViewSet(ViewSet):

    @staticmethod
    def retrieve(self):
        return Response(data={'data': 'ok'})