from random import randint

import requests
from django.utils.text import slugify

from v1.integrations.zapier.models import Zapier, ZapierWebhookTrigger


def post_to_zapier(instance, zapier):
    from v1.core.serializers import ChangelogSerializerForZapier

    data = ChangelogSerializerForZapier(instance=instance).data

    if zapier.zapier_webhook_url:
        response = requests.post(zapier.zapier_webhook_url, data=data)
        ZapierWebhookTrigger.objects.create(zapier=zapier,
                                            changelog=instance,
                                            zapier_response_status_code=response.status_code,
                                            zapier_response=response.content)


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
