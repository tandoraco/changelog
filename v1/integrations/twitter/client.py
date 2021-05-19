import tweepy
from django.conf import settings
from sentry_sdk import capture_exception
from tweepy import TweepError


class TwitterClient:

    def __init__(self, twitter_obj):
        auth = tweepy.OAuthHandler(
            twitter_obj.consumer_key,
            twitter_obj.consumer_secret
        )
        auth.set_access_token(
            twitter_obj.access_token,
            twitter_obj.access_token_secret
        )

        self.api = tweepy.API(auth)

    def send_to_twitter(self, tweet):
        try:
            response = self.api.update_status(status=tweet)
        except TweepError:
            capture_exception()
        else:
            if settings.DEBUG:
                print(response)
            else:
                pass  # Todo log
