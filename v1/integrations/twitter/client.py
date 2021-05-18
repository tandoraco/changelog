import tweepy
from django.conf import settings


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
        response = self.api.update_status(status=tweet)
        if settings.DEBUG:
            print(response)
        else:
            pass  # Todo log
