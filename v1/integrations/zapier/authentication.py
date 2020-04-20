from v1.accounts.authentication import BasicAuthentication
from v1.integrations.zapier.models import Zapier


class ZapierAPIKeyAuthentication(BasicAuthentication):

    def authenticate(self, request):
        api_key = request.query_params.get('api_key')
        if not api_key:
            api_key = request.META.get('HTTP_API_KEY')

        if api_key:
            try:
                zapier = Zapier.objects.get(api_key=api_key)
                return zapier.company.admin, zapier.company.admin.email
            except Zapier.DoesNotExist:
                return None
        else:
            return None
