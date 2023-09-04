from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class SampleViewSet(ViewSet):

    @staticmethod
    def retrieve(self):
        return Response(data={'data': 'ok'})
