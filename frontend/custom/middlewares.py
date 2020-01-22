import requests
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from frontend.views.app.public_helpers import render_html_string_without_context
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
                if request.path.startswith('/staff') or request.path.startswith('staff'):
                    raise Http404
                elif request.path == '' or request.path == '/':
                    public_index = f'{custom_domain.company.company_name}/' \
                        f'{custom_domain.company.changelog_terminology}' \
                        .lower()
                    response = requests.get(f'{settings.HOST}{public_index}')
                    return render_html_string_without_context(response.content)
                else:
                    response = requests.get(request.path)
                    return render_html_string_without_context(response.content)
            else:
                pass

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return HttpResponse(status=404)
