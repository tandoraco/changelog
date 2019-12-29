from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from v1.static_site.serializers import BulkStaticSiteFieldSerializer
from v1.utils import serializer_error_response


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
