import uuid as uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from v1.integrations.constants import NEW_CHANGELOG_TEXT, CHANGELOG_PUBLISHED_TEXT

SLACK_OAUTH_TIME_IN_MINUTES = 10


class Slack(models.Model):
    active = models.BooleanField(default=False)
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    channel_to_post = models.CharField(max_length=100, default='#random')
    oauth_response = models.JSONField(default=dict)
    trigger_when_created = models.BooleanField(default=False, help_text=NEW_CHANGELOG_TEXT)
    trigger_when_published = models.BooleanField(default=False, help_text=CHANGELOG_PUBLISHED_TEXT)

    @property
    def bot_token(self):
        return self.oauth_response.get('access_token')

    @property
    def oauth_done(self):
        return self.oauth_response

    def get_channels_list(self):
        client = WebClient(token=self.bot_token)
        try:
            channels = client.conversations_list(types='public_channel')
            channels = list(map(lambda c: f'#{c["name"]}', channels.data['channels']))
        except SlackApiError:
            channels = ['#general', '#random', ]

        return [(c, c) for c in channels]

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
