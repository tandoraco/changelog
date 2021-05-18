from random import randint

import requests
from django.forms import model_to_dict
from django.utils.text import slugify

from v1.integrations.background_tasks import trigger_integration_background_tasks
from v1.integrations.zapier.models import Zapier, ZapierWebhookTrigger
from v1.utils import random_uuid


def post_to_zapier(instance, zapier):
    from v1.core.serializers import ChangelogSerializerForZapier

    data = ChangelogSerializerForZapier(instance=instance).data

    if zapier.zapier_webhook_url:
        response = requests.post(zapier.zapier_webhook_url, data=data)
        ZapierWebhookTrigger.objects.create(zapier=zapier,
                                            changelog=instance,
                                            zapier_response_status_code=response.status_code,
                                            zapier_response=response.content)


def post_webhook(instance, webhook):
    from v1.integrations.webhooks.models import WebhookLogs

    payload = model_to_dict(instance, exclude=['company', ])
    if webhook.active:
        _hash = random_uuid().replace('-', '')
        response = requests.post(webhook.url, data=payload, headers={'TANDORA_HASH': _hash})
        WebhookLogs.objects.create(webhook=webhook,
                                   payload=payload,
                                   status_code=response.status_code,
                                   response=response.content.decode(),
                                   hash=_hash)


def get_or_populate_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{slugify(instance.title[0:190])}-{randint(0, 5000)}'


def trigger_zapier_webhook(sender, instance, created, **kwargs):
    from v1.integrations.zapier.models import NEW_CHANGELOG, CHANGELOG_PUBLISHED

    zapier = None
    try:
        if instance.company.zapier:
            zapier = instance.company.zapier
            if not zapier.active:
                raise Zapier.DoesNotExist
    except Zapier.DoesNotExist:
        pass
    else:
        if created:
            if zapier.zapier_trigger_scenario == NEW_CHANGELOG:
                post_to_zapier(instance, zapier)
            elif zapier.zapier_trigger_scenario == CHANGELOG_PUBLISHED and instance.published:
                post_to_zapier(instance, zapier)
        elif zapier.zapier_trigger_scenario == CHANGELOG_PUBLISHED and instance.published:
            try:
                ZapierWebhookTrigger.objects.get(changelog=instance)
            except ZapierWebhookTrigger.DoesNotExist:
                post_to_zapier(instance, zapier)


def trigger_webhook(sender, instance, created, **kwargs):
    from v1.integrations.webhooks.models import Webhooks

    webhook = None
    try:
        webhook = Webhooks.objects.get(company=instance.company, active=True)
    except Webhooks.DoesNotExist:
        pass
    else:
        if created and webhook.trigger_when_created:
            post_webhook(instance, webhook)
        elif webhook.trigger_when_published and instance.published:
            post_webhook(instance, webhook)


def run_integration_background_tasks(sender, instance, created, **kwargs):
    trigger_integration_background_tasks(instance.company.id, instance.id, created=created)
