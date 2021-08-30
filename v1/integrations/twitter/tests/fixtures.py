from v1.integrations.twitter.models import Twitter


def twitter_account(company):
    return Twitter.objects.create(
        company=company,
        active=True,
        access_token='dfdfdfdf',
        access_token_secret='dsdcfjenddnfdfkejdfdjf',
        consumer_key='dcvhdffvdhfid',
        consumer_secret='dfdfgdfdfgf',
        tweet_content='{title}',
        tweet_when_created=True,
        tweet_when_published=True
    )
