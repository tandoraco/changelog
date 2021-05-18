from v1.integrations.handlers import IntegrationHandlerBase, IntegrationSettingsHandlerBase
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
