from django.db import models

from v1.utils import random_uuid

CHANGELOG_PUBLISHED = 'pu'
NEW_CHANGELOG = 'ne'

ZAPIER_TRIGGER_CHOICES = (
    (CHANGELOG_PUBLISHED, 'Whenever a changelog is published for the first time'),
    (NEW_CHANGELOG, 'Whenever a changelog is created whether it is published or not')
)
ZAPIER_TRIGGER_LABEL = ('When to trigger the zapier webhook?')


class Zapier(models.Model):
    active = models.BooleanField(default=False)
    api_key = models.UUIDField(default=random_uuid, db_index=True)
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    zapier_webhook_url = models.URLField(blank=True, null=True)
    zapier_trigger_scenario = models.CharField(max_length=2, choices=ZAPIER_TRIGGER_CHOICES,
                                               default=NEW_CHANGELOG,
                                               help_text=ZAPIER_TRIGGER_LABEL)

    def __str__(self):
        return f'Zapier integration -> company {self.company}, active: {self.active}'


class ZapierWebhookTrigger(models.Model):
    zapier = models.ForeignKey('Zapier', on_delete=models.CASCADE)
    changelog = models.OneToOneField('Changelog', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    zapier_response_status_code = models.PositiveIntegerField(blank=False, null=False)
    zapier_response = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'{self.zapier_response_status_code} - {self.created_time}'
