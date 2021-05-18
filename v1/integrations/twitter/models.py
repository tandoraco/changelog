from django.db import models

from v1.integrations.constants import NEW_CHANGELOG_TEXT, CHANGELOG_PUBLISHED_TEXT
from v1.integrations.twitter.constants import DEFAULT_TWEET_CONTENT


class Twitter(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    access_token = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)
    consumer_key = models.CharField(max_length=100)
    consumer_secret = models.CharField(max_length=100)
    tweet_content = models.TextField(max_length=280, default=DEFAULT_TWEET_CONTENT)
    tweet_when_created = models.BooleanField(default=False, help_text=NEW_CHANGELOG_TEXT)
    tweet_when_published = models.BooleanField(default=False, help_text=CHANGELOG_PUBLISHED_TEXT)

    def __str__(self):
        return f'{self.company} -> Twitter active: {self.active}'
