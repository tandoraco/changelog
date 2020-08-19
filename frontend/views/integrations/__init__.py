from collections import namedtuple

import stringcase as stringcase
from django import forms
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from frontend.constants import INTEGRATION_NOT_AVAILABLE_FOR_PLAN_ERROR, INTEGRATION_EDITED_SUCCESSFULLY, \
    INTEGRATION_EDIT_FAILED_ERROR, NOT_ALLOWED
from frontend.custom import views as custom_views
from frontend.custom.decorators import is_authenticated, is_admin
from frontend.custom.forms import TandoraForm
from v1.accounts.models import Subscription

integration_meta = namedtuple('integration_meta', 'name logo description')

INTEGRATION_FORM_FIELDS_DICT = {
    'zapier': {
        'read_only_fields': ['api_key'],
        'exclude': ['company', 'zapier_webhook_url', ]
    }
}

INTEGRATION_FRONTEND_META_DICT = {
    'zapier': {
        'logo': 'https://tandora-production.s3.amazonaws.com/assets/logos/zapier-logo.png',
        'description': 'Zapier provides workflows to automate the use of web applications together. '
                       'You can connect your favorite apps like Twitter, Facebook etc with Tandora '
                       'Changelog using Zapier Integration.'
                       'This enables you to seamlessly post Tandora Changelog to all of the connected Zapier Apps.'
                       'In a nutshell you can create a changelog once and post it to any of the connected Zapier Apps '
                       'using this integration.'
                       '<a href="/staff/manage/integrations/zapier/embed">Click here</a> '
                       'to view list of zaps available.'
    }
}


INTEGRATION_EMBED_DICT = {
    'zapier': {
        'title': 'Tandora Changelog Zaps',
        'embed': '<script src="https://zapier.com/apps/embed/widget.js?services=tandora-changelog&limit=10"></script>'
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
        return INTEGRATION_FRONTEND_META_DICT.keys()


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
    model_class = apps.get_model('v1', stringcase.pascalcase(integration))
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


@is_authenticated
@is_admin
def embed_details(request, integration):
    try:
        context = INTEGRATION_EMBED_DICT[integration.lower()]
        return render(request, 'staff/integration-embed.html', context=context)
    except KeyError:
        raise Http404
