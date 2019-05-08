from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from v1.settings import helpers as settings_helpers


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def settings(request):
    # Todo: add billing, team details and widget
    return_data = {
        'company': settings_helpers.get_company(),
        'user_profile': settings_helpers.get_user(request.user.email),
        'categories': settings_helpers.get_categories(),
        'public_page': settings_helpers.get_public_page()
    }
    return Response(status=HTTP_200_OK, data=return_data)
