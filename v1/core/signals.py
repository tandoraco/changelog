from random import randint

import requests
from django.conf import settings
from django.utils.text import slugify

from v1.integrations.zapier.models import Zapier


def get_or_populate_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{slugify(instance.title[0:190])}-{randint(0, 5000)}'


def trigger_zapier_webhook(sender, instance, created, **kwargs):
    from v1.core.serializers import ChangelogSerializer
    if created:
        try:
            if instance.company.zapier:
                zapier = instance.company.zapier
                if zapier.active and zapier.zapier_webhook_url:
                    data = ChangelogSerializer(instance=instance).data
                    data['company'] = slugify(instance.company.company_name)
                    data['changelog_terminology'] = slugify(instance.company.changelog_terminology)
                    data['view_url'] = \
                        f"{settings.HOST}{data['company']}/{data['changelog_terminology']}/{instance.slug}"
                    requests.post(zapier.zapier_webhook_url, data=data)
        except Zapier.DoesNotExist:
            pass
