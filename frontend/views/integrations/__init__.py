from django import forms
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from frontend.constants import INTEGRATION_NOT_AVAILABLE_FOR_PLAN_ERROR, INTEGRATION_EDITED_SUCCESSFULLY, \
    INTEGRATION_EDIT_FAILED_ERROR, NOT_ALLOWED
from frontend.custom import views as custom_views
from frontend.custom.decorators import is_authenticated, is_admin
from frontend.custom.forms import TandoraForm
from v1.accounts.models import Subscription


INTEGRATION_FORM_FIELDS_DICT = {
    'zapier': {
        'read_only_fields': ['api_key', 'zapier_webhook_url'],
        'exclude': ['company', ]
    }
}


def uuid_form_value(self, value):
    # Patching UUIDField of forms here
    # This is because django form converts uuid field value to hex.
    # In zapier integration, we want users to copy api key from frontend
    # Without patching api key will appear as hex in frontend.
    # So patching the field so that original uuid value appears in frontend
    return value


class IntegrationList(custom_views.TandoraAdminListViewMixin):
    template_name = 'staff/integrations/index.html'

    def get_queryset(self):
        return INTEGRATION_FORM_FIELDS_DICT.keys()


@is_authenticated
@is_admin
def integration_form(request, integration):
    if request.user.company.is_static_site:
        messages.info(request, NOT_ALLOWED)
        return HttpResponseRedirect('/staff')

    try:
        subscription = request.user.company.subscription
        if not subscription.all_plan_features.get(integration):
            raise Subscription.DoesNotExist
    except Subscription.DoesNotExist:
        messages.warning(request, INTEGRATION_NOT_AVAILABLE_FOR_PLAN_ERROR)
        return HttpResponseRedirect(reverse('frontend-view-integrations'))

    model_class = apps.get_model('v1', integration.replace('_', '').title())
    instance, created = model_class.objects.get_or_create(company=request.user.company)
    integration_field_meta = INTEGRATION_FORM_FIELDS_DICT.get(integration, {})

    forms.UUIDField.prepare_value = uuid_form_value

    class IntegrationModelForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            super(IntegrationModelForm, self).__init__(*args, **kwargs)

            for field in integration_field_meta.get('read_only_fields', []):
                self.fields[field].disabled = True

        class Meta:
            model = model_class
            if integration_field_meta.get('exclude'):
                exclude = integration_field_meta['exclude']
            elif integration_field_meta.get('fields'):
                fields = integration_field_meta['fields']
            else:
                fields = '__all__'

    return TandoraForm(model_class, IntegrationModelForm, 'edit', 'staff/form.html',
                       reverse('frontend-view-integrations')) \
        .get_form(request,
                  success_message=INTEGRATION_EDITED_SUCCESSFULLY,
                  error_message=INTEGRATION_EDIT_FAILED_ERROR, instance=instance)
