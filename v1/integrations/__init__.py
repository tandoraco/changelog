from v1.integrations.zapier import handlers as zapier_handler
from v1.integrations.webhooks import handlers as webhooks_handler
from v1.integrations.twitter import handlers as twitter_handler

INTEGRATION_MAP = {
    'zapier': zapier_handler.ZapierHandler,
    'webhooks': webhooks_handler.WebhooksHandler,
    'twitter': twitter_handler.TwitterHandler,
}

INTEGRATION_SETTINGS_MAP = {
    'zapier': zapier_handler.ZapierSettingsHandler,
    'webhooks': webhooks_handler.WebhookSettingsHandler,
    'twitter': twitter_handler.TwitterSettingsHandler,
}
