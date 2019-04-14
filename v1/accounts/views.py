from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from v1.accounts import serializers as accounts_serializers
from v1.accounts.authentication import BasicAuthentication
from v1.accounts.permissions import IsAdmin
from v1.utils import serializer_error_response


@api_view(["POST"])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, IsAdmin])
def create_user(request):
    serializer = accounts_serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = {
            'email': user.email,
        }
        return Response(status=status.HTTP_201_CREATED, data=data)

    return serializer_error_response(serializer)


@api_view(["POST"])
@authentication_classes([])  # Empty because, company can be created without authentication.
def create_company(request):
    # Creates a company and adds an admin.
    serializer = accounts_serializers.CompanySerializer(data=request.data)
    if serializer.is_valid():
        company = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={
            'id': company.id,
            'admin': company.admin.email,
            'company_name': company.company_name,
            'changelog_terminology': company.changelog_terminology
        })

    return serializer_error_response(serializer)


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
