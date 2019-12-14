from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from v1.core.models import Changelog
from v1.core.serializers import ChangelogSerializer, BulkStaticSiteFieldSerializer
from v1.utils import serializer_error_response
from v1.utils.viewsets import TandoraModelViewSet


class ChangelogViewSet(TandoraModelViewSet):
    queryset = Changelog.objects.all()
    serializer_class = ChangelogSerializer

    def create(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk
        return super(ChangelogViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk

        return super(ChangelogViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk

        return super(ChangelogViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk
            request.data["deleted"] = True

        return super(ChangelogViewSet, self).destroy(request, *args, **kwargs)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def bulk_create_static_site_fields_from_json(request):
    serializer = BulkStaticSiteFieldSerializer(data=request.data)

    if serializer.is_valid():
        fields = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={
            "field_ids": [field.id for field in fields]
        })

    return serializer_error_response(serializer)
