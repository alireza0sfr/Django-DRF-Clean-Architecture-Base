from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
          'success': False,
          'data': None,
          'message': ''
        }

        if str(status_code).startswith('2'):
            response['success'] = True
            response['data'] = data
            try:
                response['message'] = renderer_context['response'].message
            except KeyError:
                response['data'] = data

        return super(CustomJSONRenderer, self).render(response, accepted_media_type, renderer_context)