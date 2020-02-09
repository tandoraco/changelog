from v1.integrations.zapier import handlers as zapier_handler

INTEGRATION_MAP = {
    'zapier': zapier_handler.ZapierHandler,
}

INTEGRATION_SETTINGS_MAP = {
    'zapier': zapier_handler.ZapierSettingsHandler,
}
