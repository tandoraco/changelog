from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from v1.accounts.models import CustomDomain


class CustomDomainMiddleware(MiddlewareMixin):

    def process_request(self, request):
        host = request.get_host()

        if 'app.tandora.co' not in host:
            try:
                custom_domain = CustomDomain.objects.get(domain_name=host, is_enabled=True)
                redirect_to = []
                for part in custom_domain.tandora_url.split('/'):
                    if part and ['http:', 'https:', 'app.tandora.co'] not in part:
                        redirect_to.append(part)
                return HttpResponseRedirect('/'.join(redirect_to))
            except CustomDomain.DoesNotExist:
                pass
