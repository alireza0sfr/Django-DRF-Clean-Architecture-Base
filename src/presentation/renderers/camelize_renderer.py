from rest_framework.renderers import JSONRenderer
from rest_framework import status
from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class CamelizeRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        exception = renderer_context['response'].exception
        
        response = {
          'success': status_code and str(status_code).startswith('2'),
          'code': status_code if status_code else status.HTTP_400_BAD_REQUEST,
          'message': data.pop('detail') if isinstance(data, dict) and data.get('detail') else '',
        }

        if exception:
            response['key'] = data.get('key') if 'key' in data else ''
            response['errors'] = data.get('errors') if 'errors' in data else data
        else:
            response['data'] = data.get('data') if isinstance(data, dict) and 'data' in data else data

        camelize = CamelCaseJSONRenderer().render(response, accepted_media_type, renderer_context)
        return camelize
