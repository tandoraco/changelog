from django.db import transaction
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from v1.accounts.authentication import FrontEndTokenAuthentication
from v1.core.models import Changelog
from v1.core.serializers import ChangelogSerializer, InlineImageAttachmentSerializer
from v1.utils import serializer_error_response
from v1.utils.viewsets import TandoraModelViewSet


class ChangelogViewSet(TandoraModelViewSet):
    serializer_class = ChangelogSerializer
    model_class = Changelog


@api_view(['POST', ])
@authentication_classes([FrontEndTokenAuthentication, TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def inline_image_attachment(request):
    file = request.FILES.get('file')
    data = {
        'company': request.user.company.id,
        'file': file
    }
    serializer = InlineImageAttachmentSerializer(data=data)

    if serializer.is_valid():
        image = serializer.save()

        return Response(status=status.HTTP_201_CREATED, data={
            'location': image.file.url
        })

    return serializer_error_response(serializer)


@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
@transaction.atomic
def increase_view_count(request, pk):
    changelog = get_object_or_404(Changelog, pk=pk)
    changelog.view_count += 1
    changelog.save()

    changelog.refresh_from_db()

    return Response(status=status.HTTP_200_OK, data={
        'view_count': changelog.view_count
    })
