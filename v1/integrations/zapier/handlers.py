from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from v1.integrations.handlers import IntegrationSettingsHandlerBase, IntegrationHandlerBase
from v1.integrations.zapier.models import Zapier
from v1.integrations.zapier.serializers import ZapierSerializer


class ZapierSettingsHandler(IntegrationSettingsHandlerBase):

    @property
    def integration_name(self):
        return 'zapier'

    @property
    def serializer_class(self):
        return ZapierSerializer

    @property
    def model_class(self):
        return Zapier


class ZapierHandler(IntegrationHandlerBase):
    model = Zapier
    serializer = ZapierSerializer

    def ping(self, request):
        if request.method != 'GET':
            raise MethodNotAllowed(request.method)

        return Response(status=status.HTTP_200_OK, data={'success': True})

    def subscribe_webhook(self, request):
        if request.method != 'POST':
            raise MethodNotAllowed(request.method)

        webhook_url = request.data.get('hookUrl')
        zapier = self.integration
        zapier.zapier_webhook_url = webhook_url
        zapier.save()

        return Response(status=status.HTTP_201_CREATED, data={'SUB': 'ok'})

    def unsubscribe_webhook(self, request):
        if request.method != 'DELETE':
            raise MethodNotAllowed(request.method)

        zapier = self.integration
        zapier.zapier_webhook_url = None
        zapier.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def list_changelogs(self, request):
        from v1.core.models import Changelog
        from v1.core.serializers import ChangelogSerializer
        changelogs = Changelog.objects.filter(company=request.user.company)[:10]
        data = ChangelogSerializer(instance=changelogs, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
