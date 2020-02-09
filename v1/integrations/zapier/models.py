from django.db import models

from v1.utils import random_uuid


class Zapier(models.Model):
    active = models.BooleanField(default=False)
    api_key = models.UUIDField(default=random_uuid, db_index=True)
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    zapier_webhook_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'Zapier integration -> company {self.company}, active: {self.active}'
