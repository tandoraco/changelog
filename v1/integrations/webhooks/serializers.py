from rest_framework.serializers import ModelSerializer

from v1.integrations.webhooks.models import WebhookLogs, Webhooks


class WebhooksSerializer(ModelSerializer):

    class Meta:
        model = Webhooks
        exclude = ('company', )


class WebhookLogsSerializer(ModelSerializer):

    class Meta:
        model = WebhookLogs
        fields = '__all__'
