from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send_message(channel, text):
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        print(response)
    except SlackApiError as e:
        print('exception')
        print(e.response)
