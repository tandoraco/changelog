from abc import abstractmethod

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.response import Response

from v1.utils import serializer_error_response

INTEGRATION_NOT_AVAILABLE_FOR_PLAN = "Your current subscription plan does not allow this integration." \
                                     "Please contact support@tandora.co for more details. "


class IntegrationSettingsHandlerBase(object):

    def __init__(self, company):
        self.company = company

    @property
    @abstractmethod
    def integration_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def serializer_class(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def model_class(self):
        raise NotImplementedError

    @property
    def is_integration_available_for_plan(self):
        from v1.accounts.models import Subscription
        try:
            return self.company.subscription and self.company.subscription.all_plan_features.get(self.integration_name)
        except Subscription.DoesNotExist:
            return False

    @transaction.atomic
    def handle(self, request):
        if not self.is_integration_available_for_plan:
            raise PermissionDenied(INTEGRATION_NOT_AVAILABLE_FOR_PLAN)

        serializer_class = self.serializer_class
        integration, created = self.model_class.objects.get_or_create(company=request.user.company)

        if request.method == 'GET':
            serializer = serializer_class(instance=integration)
            data = serializer.data
            data['name'] = self.integration_name
            return Response(status=status.HTTP_200_OK, data=data)
        elif request.method == 'PATCH':
            data = request.data
            data['company'] = request.user.company.id
            serializer = serializer_class(instance=integration, data=data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data['name'] = self.integration_name
                return Response(status=status.HTTP_200_OK, data=data)
            else:
                return serializer_error_response(serializer)
        else:
            raise MethodNotAllowed
