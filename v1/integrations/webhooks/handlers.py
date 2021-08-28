from rest_framework import status

from v1.integrations.handlers import IntegrationSettingsHandlerBase, IntegrationHandlerBase, BackgroundJobHandlerBase
from v1.integrations.webhooks.client import WebhookClient
from v1.integrations.webhooks.models import Webhooks
from v1.integrations.webhooks.serializers import WebhooksSerializer

from rest_framework.response import Response


class WebhookSettingsHandler(IntegrationSettingsHandlerBase):
    @property
    def integration_name(self):
        return 'webhooks'

    @property
    def serializer_class(self):
        return WebhooksSerializer

    @property
    def model_class(self):
        return Webhooks


class WebhooksHandler(IntegrationHandlerBase):
    model = Webhooks
    serializer = WebhooksSerializer

    def trigger_test(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)


class WebhookBackgroundJobHandler(BackgroundJobHandlerBase):

    def execute(self, **kwargs):
        client = WebhookClient(self.integration_object, self.changelog)

        if kwargs.get('created') and self.integration_object.trigger_when_created:
            client.post_webhook()
        elif self.integration_object.trigger_when_published and self.changelog.published:
            client.post_webhook()
