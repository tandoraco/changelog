import requests
from django.conf import settings
from django.forms import model_to_dict

from v1.integrations.webhooks.models import WebhookLogs
from v1.utils import random_uuid


class WebhookClient:

    def __init__(self, webhook_obj, changelog):
        self.webhook_obj = webhook_obj
        self.changelog = changelog
        self.hash = random_uuid().replace('-', '')

    def create_webhook_log(self, payload, response):
        WebhookLogs.objects.create(webhook=self.webhook_obj,
                                   payload=payload,
                                   status_code=response.status_code,
                                   response=response.content.decode(),
                                   hash=self.hash)

    def post_webhook(self):
        payload = model_to_dict(self.changelog, exclude=['company', ])
        if self.webhook_obj.active:
            response = requests.post(self.webhook_obj.url, data=payload, headers={'TANDORA_HASH': self.hash})
            self.create_webhook_log(payload, response)
            if settings.DEBUG:
                print(response)
            else:
                pass  # Todo: Log
        else:
            pass  # Todo: Log
