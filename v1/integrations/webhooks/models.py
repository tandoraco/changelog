from django.db import models
from payanpaadu.webhooks.models import Webhook, WebhookLog

from v1.integrations.constants import NEW_CHANGELOG_TEXT, CHANGELOG_PUBLISHED_TEXT


class Webhooks(Webhook):
    company = models.OneToOneField('Company', on_delete=models.DO_NOTHING)
    trigger_when_created = models.BooleanField(default=False, help_text=NEW_CHANGELOG_TEXT)
    trigger_when_published = models.BooleanField(default=False, help_text=CHANGELOG_PUBLISHED_TEXT)


class WebhookLogs(WebhookLog):
    webhook = models.ForeignKey('Webhooks', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.webhook} - {self.status_code}'
