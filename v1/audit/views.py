from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from v1.accounts.models import Company
from v1.audit.helpers import audit_public_page_request
from v1.audit.serializers import PublicPageViewSerializer


@api_view(['PATCH', ])
@authentication_classes([])
@permission_classes([])
@transaction.atomic
def record_public_page_view(request):
    serializer = PublicPageViewSerializer(data=request.data)

    if serializer.is_valid():
        company_name = serializer.validated_data['company_name']
        get_object_or_404(Company, company_name__iexact=company_name)
        audit_public_page_request(request, company_name)
        return Response(status=status.HTTP_200_OK, data=[])

    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=serializer.errors)
