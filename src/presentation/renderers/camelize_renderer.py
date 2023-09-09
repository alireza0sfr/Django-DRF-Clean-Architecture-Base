from rest_framework.renderers import JSONRenderer
from rest_framework import status
from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class CamelizeRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        message = ''

        if(data.get('message')):
            message = data.get('message')
            data.pop('message')

        response = {
          'success': status_code and str(status_code).startswith('2'),
          'code': status_code if status_code else status.HTTP_400_BAD_REQUEST,
          'message': message,
          'data': data.get('data') if data.get('data') else data,
        }

        camelize = CamelCaseJSONRenderer().render(response, accepted_media_type, renderer_context)
        return camelize
