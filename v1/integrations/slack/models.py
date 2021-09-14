import uuid as uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone

SLACK_OAUTH_TIME_IN_MINUTES = 10


class Slack(models.Model):
    active = models.BooleanField(default=False)
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    channel_to_post = models.CharField(max_length=100, default='#random')
    oauth_response = models.JSONField(default={})

    @property
    def bot_token(self):
        return self.oauth_response.get('access_token')

    def __str__(self):
        return f'{self.company} - {self.active}'


class SlackState(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=SLACK_OAUTH_TIME_IN_MINUTES)

    def __str__(self):
        return str(self.uuid)
