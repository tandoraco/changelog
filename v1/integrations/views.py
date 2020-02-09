from knox.auth import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from v1.accounts.authentication import FrontEndTokenAuthentication
from v1.accounts.permissions import IsAdmin
from v1.integrations import INTEGRATION_MAP, INTEGRATION_SETTINGS_MAP


@api_view(['GET', 'PATCH'])
@authentication_classes([FrontEndTokenAuthentication, TokenAuthentication, ])
@permission_classes([IsAuthenticated, IsAdmin, ])
def integration_settings(request, integration_name):
    try:
        integration_settings_handler = INTEGRATION_SETTINGS_MAP[integration_name]
        return integration_settings_handler(company=request.user.company).handle(request)
    except KeyError:
        raise NotFound


@authentication_classes([FrontEndTokenAuthentication, TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def integration_action(request, integration_name, action):
    try:
        integration_handler = INTEGRATION_MAP[integration_name](company=request.user.company)
        action = action.replace('-', '_').strip()
        integration_action_handler = getattr(integration_handler, action)
        return integration_action_handler(request)
    except (KeyError, AttributeError):
        raise NotFound
