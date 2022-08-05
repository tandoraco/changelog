from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from sentry_sdk.integrations.wsgi import get_client_ip

from v1.links.models import Link, LinkLens


@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
@transaction.atomic
def track_link_click(request, pk):
    link = get_object_or_404(Link, pk=pk)

    if request.user_agent.is_mobile:
        device_type = 'mo'
    elif request.user_agent.is_tablet:
        device_type = 'tb'
    elif request.user_agent.is_pc:
        device_type = 'pc'
    elif request.user_agent.is_bot:
        device_type = 'bo'
    else:
        device_type = None

    data = {
        'link': link,
        'ip_address': get_client_ip(request.META),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'device_type': device_type
    }
    LinkLens.objects.create(**data)

    return Response(status=status.HTTP_204_NO_CONTENT)
