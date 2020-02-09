from v1.integrations.handlers import IntegrationSettingsHandlerBase
from v1.integrations.zapier.models import Zapier
from v1.integrations.zapier.serializers import ZapierSerializer


class ZapierSettingsHandler(IntegrationSettingsHandlerBase):

    @property
    def integration_name(self):
        return 'zapier'

    @property
    def serializer_class(self):
        return ZapierSerializer

    @property
    def model_class(self):
        return Zapier


class ZapierHandler:
    pass
