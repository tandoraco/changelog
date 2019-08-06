from django.utils.deprecation import MiddlewareMixin


class DBSwitchMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(f'request url and subdomain: {request.META["HTTP_HOST"]}')
