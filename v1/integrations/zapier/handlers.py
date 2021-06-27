import requests
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from v1.audit.actions import AuditLogAction
from v1.integrations.handlers import IntegrationSettingsHandlerBase, IntegrationHandlerBase, BackgroundJobHandlerBase
from v1.integrations.zapier.models import Zapier, ZapierWebhookTrigger, NEW_CHANGELOG, CHANGELOG_PUBLISHED
from v1.integrations.zapier.serializers import ZapierSerializer


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
            changelog = serializer.save()
            from v1.core.serializers import ChangelogSerializerForZapier
            data = ChangelogSerializerForZapier(changelog).data
            AuditLogAction(request, changelog, 'zapier').set_audit_log()
            return Response(status=status.HTTP_201_CREATED, data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.custom_full_errors_str)

    def poll(self, request):
        if request.method != 'GET':
            raise MethodNotAllowed(request.method)
        try:
            from v1.core.models import Changelog
            from v1.core.serializers import ChangelogSerializerForZapier
            changelog = Changelog.objects.filter(
                company=self.company,
                published=True,
                deleted=False).order_by('-created_at')[0]
            data = ChangelogSerializerForZapier(changelog).data
            return Response(status=status.HTTP_200_OK, data=[data])
        except IndexError:
            return Response(status=status.HTTP_200_OK, data=[])


class ZapierBackgroundJobHandler(BackgroundJobHandlerBase):

    def create_zapier_webhook_trigger(self, response):
        ZapierWebhookTrigger.objects.create(zapier=self.integration_object,
                                            changelog=self.changelog,
                                            zapier_response_status_code=response.status_code,
                                            zapier_response=response.content)

    def trigger_zapier_webhook(self, data):
        if self.integration_object.zapier_webhook_url:
            response = requests.post(self.integration_object.zapier_webhook_url, data=data)
            self.create_zapier_webhook_trigger(response)
        else:
            pass  # Todo Log

    def execute(self, **kwargs):
        from v1.core.serializers import ChangelogSerializerForZapier
        data = ChangelogSerializerForZapier(instance=self.changelog).data

        if kwargs.get('created') and self.integration_object.zapier_trigger_scenario == NEW_CHANGELOG:
            self.trigger_zapier_webhook(data)
        elif self.integration_object.zapier_trigger_scenario == CHANGELOG_PUBLISHED and self.changelog.published:
            try:
                ZapierWebhookTrigger.objects.get(changelog=self.changelog)
            except ZapierWebhookTrigger.DoesNotExist:
                self.trigger_zapier_webhook(data)
