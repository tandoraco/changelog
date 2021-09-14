from django.urls import path

from v1.integrations.slack.views import slack_oauth_start, slack_oauth_callback

urlpatterns = [
    path('/oauth/start/', slack_oauth_start, name='slack-oauth-start'),
    path('/oauth/callback/', slack_oauth_callback, name='slack-oauth-callback'),
]
