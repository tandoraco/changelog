from urllib.parse import urljoin

from django.conf import settings
from django.utils.text import slugify

from v1.integrations.handlers import IntegrationHandlerBase, IntegrationSettingsHandlerBase, BackgroundJobHandlerBase
from v1.integrations.twitter.client import TwitterClient
from v1.integrations.twitter.constants import TWEET_SUBSTITUTES_MAP
from v1.integrations.twitter.models import Twitter
from v1.integrations.twitter.serializers import TwitterSerializer


class TwitterSettingsHandler(IntegrationSettingsHandlerBase):
    @property
    def integration_name(self):
        return 'twitter'

    @property
    def serializer_class(self):
        return TwitterSerializer

    @property
    def model_class(self):
        return Twitter


class TwitterHandler(IntegrationHandlerBase):
    pass


class TwitterBackgroundJobHandler(BackgroundJobHandlerBase):

    def get_title(self):
        return self.changelog.title

    def get_content(self):
        return self.changelog.content

    def get_category(self):
        return self.changelog.category.name

    def get_link(self):
        link = urljoin(settings.HOST,
                       f'{slugify(self.company.company_name)}/'
                       f'{slugify(self.company.changelog_terminology)}/'
                       f'{self.changelog.slug}')
        return link

    def substitute_tweet(self):
        tweet_content = self.integration_object.tweet_content
        for attr_name, func in TWEET_SUBSTITUTES_MAP.items():
            tweet_content = tweet_content.replace(attr_name, getattr(self, func)())
        return tweet_content

    def execute(self, **kwargs):
        tweet = self.substitute_tweet()

        twitter_client = TwitterClient(self.integration_object)
        if kwargs.get('created') and self.integration_object.tweet_when_created:
            twitter_client.send_to_twitter(tweet)
        elif self.integration_object.tweet_when_published and self.changelog.published:
            twitter_client.send_to_twitter(tweet)
