from django.db import models
from payanpaadu.webhooks.models import Webhook, WebhookLog

from v1.integrations.constants import TRIGGER_CHOICES


class Webhooks(Webhook):
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING)
    trigger_event = models.CharField(max_length=2, choices=TRIGGER_CHOICES)
    categories = models.ManyToManyField('Category')


class WebhookLogs(WebhookLog):
    webhook = models.ForeignKey('Webhooks', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.webhook} - {self.status_code}'
