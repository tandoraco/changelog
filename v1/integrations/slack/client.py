from slack_sdk import WebClient

from v1.utils import html_2_text


class SlackClient:

    def __init__(self, instance, changelog):
        self.instance = instance
        self.changelog = changelog

    def get_text(self):
        return f'{self.changelog.title} \n {html_2_text(self.changelog.content)}'

    def post_message(self):
        client = WebClient(token=self.instance.bot_token)
        client.chat_postMessage(channel=self.instance.channel_to_post, text=self.get_text())
