from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from v1.integrations.handlers import IntegrationSettingsHandlerBase, IntegrationHandlerBase
from v1.integrations.zapier.models import Zapier
from v1.integrations.zapier.serializers import ZapierSerializer
from v1.utils import serializer_error_response


class ZapierSettingsHandler(IntegrationSettingsHandlerBase):

    @property
    def integration_name(self):
        return 'zapier'

    @property
    def serializer_class(self):
        return ZapierSerializer

    @property
    def model_class(self):
        return Zapier


class ZapierHandler(IntegrationHandlerBase):
    model = Zapier
    serializer = ZapierSerializer

    def ping(self, request):
        if request.method != 'GET':
            raise MethodNotAllowed(request.method)

        return Response(status=status.HTTP_200_OK, data={'success': True, 'email': self.company.admin.email,
                                                         'company': self.company.company_name})

    def subscribe_webhook(self, request):
        if request.method != 'POST':
            raise MethodNotAllowed(request.method)

        webhook_url = request.data.get('hookUrl')
        zapier = self.integration
        zapier.zapier_webhook_url = webhook_url
        zapier.save()

        return Response(status=status.HTTP_201_CREATED, data={'SUB': 'ok'})

    def unsubscribe_webhook(self, request):
        if request.method != 'DELETE':
            raise MethodNotAllowed(request.method)

        zapier = self.integration
        zapier.zapier_webhook_url = None
        zapier.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def category_metadata(self, request):
        if request.method != 'GET':
            raise MethodNotAllowed(request.method)

        # https://github.com/zapier/zapier-platform/blob/zapier-platform-schema@9.1.0/packages/schema/lib/schemas/FieldSchema.js
        # Refer above link for data structure
        from v1.categories.models import Category
        categories = Category.objects.filter(company=self.company, deleted=False)

        data = {
            'key': 'category',
            'choices': []
        }

        for category in categories:
            data['choices'].append({
                'label': category.name,
                'sample': category.id,
                'value': category.id
            })

        return Response(status=status.HTTP_200_OK, data=data)

    def create_changelog(self, request):
        if request.method != 'POST':
            raise MethodNotAllowed(request.method)

        data = request.data.copy()
        data['company'] = self.company.id
        data['created_by'] = self.company.admin.id
        data['last_edited_by'] = self.company.admin.id
        from v1.core.serializers import ChangelogSerializer
        serializer = ChangelogSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'success': True})
        else:
            return serializer_error_response(serializer)
