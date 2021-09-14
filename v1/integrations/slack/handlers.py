from v1.integrations.handlers import BackgroundJobHandlerBase
from v1.integrations.slack.client import SlackClient


class SlackBackgroundJobHandler(BackgroundJobHandlerBase):
    def execute(self, **kwargs):
        slack_client = SlackClient(self.integration_object, self.changelog)
        if kwargs.get('created') and self.integration_object.trigger_when_created:
            slack_client.post_message()
        elif self.integration_object.trigger_when_published and self.changelog.published:
            slack_client.post_message()
