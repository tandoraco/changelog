import requests
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin
from django.utils.text import slugify

from v1.accounts.models import CustomDomain


class CustomDomainMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if settings.DEBUG or settings.TESTING:
            pass
        else:
            try:
                host_domain = request.META['HTTP_HOST']
            except KeyError:
                host_domain = request.META.get('HOST')
            print(f'host domain {host_domain}')
            print(f'request path {request.path}')
            if host_domain and 'app.tandora.co' not in host_domain:
                host_domain = host_domain.replace('http://', '').replace('https://', '').split('/')[0]
                custom_domain = get_object_or_404(CustomDomain, domain_name__contains=host_domain)
                company_name = slugify(custom_domain.company.company_name.lower())
                changelog_terminology = slugify(custom_domain.company.changelog_terminology.lower())
                request_path = request.path.lower()
                if request_path.startswith('/staff') or request_path.startswith('staff'):
                    raise Http404
                elif request_path == '' or request_path == '/':
                    response = requests.get(custom_domain.tandora_url)
                    print('1')
                    print(response)
                    print(response.content)
                    return response
                elif company_name in request_path and changelog_terminology in request_path:
                    path = request.path
                    if path.startswith('/'):
                        path = path[1:]
                    url = f'{settings.HOST}{path}'
                    response = requests.get(url)
                    print(2)
                    print(response)
                    print(response.content)
                    return response
                else:
                    pass
            else:
                pass

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return HttpResponse(status=404)
