import uuid

from django.db import models
from payanpaadu.webhooks.models import Webhook, WebhookLog

from v1.integrations.constants import NEW_CHANGELOG_TEXT, CHANGELOG_PUBLISHED_TEXT

PUBLISHED_VALUE_HELP_TEXT = 'If published mapping is not set, ' \
                            'then this will be given preference when creating changelog to decide ' \
                            'whether it should be published or not.'


class Webhooks(Webhook):
    company = models.OneToOneField('Company', on_delete=models.DO_NOTHING)
    trigger_when_created = models.BooleanField(default=False, help_text=NEW_CHANGELOG_TEXT)
    trigger_when_published = models.BooleanField(default=False, help_text=CHANGELOG_PUBLISHED_TEXT)


class WebhookLogs(WebhookLog):
    webhook = models.ForeignKey('Webhooks', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.webhook} - {self.status_code}'


class IncomingWebhook(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    hash = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    title_mapping = models.CharField(max_length=50)
    content_mapping = models.CharField(max_length=50)
    published_mapping = models.CharField(max_length=50, null=True, blank=True)
    published_value = models.BooleanField(default=True, help_text=PUBLISHED_VALUE_HELP_TEXT)
    featured_image_mapping = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class IncomingWebhookLog(WebhookLog):
    incoming_webhook = models.ForeignKey('IncomingWebhook', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.incoming_webhook.company} - {self.status_code}'
