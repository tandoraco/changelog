from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from frontend.constants import (WIDGET_DOES_NOT_EXIST,
                                WIDGET_CREATED_OR_EDITED_SUCCESSFULLY,
                                WIDGET_CODE_EDIT_WARNING, NOT_ALLOWED)
from frontend.custom.decorators import is_authenticated
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import get_company_from_slug_and_changelog_terminology
from frontend.forms.auth.utils import get_plan_features
from frontend.forms.widget import WidgetForm
from v1.accounts.models import Company
from v1.core.models import Changelog
from v1.widget.models import Embed


INITIAL_JAVASCRIPT = f'<script>\n /* {WIDGET_CODE_EDIT_WARNING} */ \n // Insert your code below \n </script>'
INITIAL_CSS = '{}'


@is_authenticated
def widget_form(request):
    company_id = request.session['company-id']
    extra = None

    company = Company.objects.get(id=company_id)
    if company.is_static_site:
        messages.info(request, NOT_ALLOWED)
        return HttpResponseRedirect('/staff')

    if Embed.objects.filter(company__id=company_id).count() == 0:
        action = 'create'
        initial = {
            'javascript': INITIAL_JAVASCRIPT,
            'css': INITIAL_CSS
        }
        id = None
    else:
        action = 'edit'
        initial = None
        embed = Embed.objects.get(company__id=company_id)
        id = embed.id

        embed_changed = False

        if not embed.css:
            embed.css = INITIAL_CSS
            embed_changed = True

        if not embed.javascript:
            embed.javascript = INITIAL_JAVASCRIPT
            embed_changed = True

        if embed_changed:
            embed.save()

        if embed.enabled:
            public_page_url = f"{request.session['public-page-url']}/widget/1"
            extra = f'<i><a target="_blank" href="{public_page_url}">Click here</a> to view widget.</i>'

    return TandoraForm(Embed, WidgetForm, action, 'staff/form.html',
                       reverse('frontend-manage-widget'), initial=initial) \
        .get_form(request, success_message=WIDGET_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=WIDGET_DOES_NOT_EXIST, id=id, extra=extra)


@csrf_exempt
@xframe_options_exempt
def public_widget(request, company, changelog_terminology):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        widget = Embed.objects.get(company=company, enabled=True)
        changelogs = Changelog.objects.filter(company=company, published=True,
                                              deleted=False).order_by('-created_at')[:10]
        return render(request, 'public/widget.html',
                      context={
                          'company': company,
                          'widget': widget,
                          'changelogs': changelogs,
                          'hide_tandora_logo': True,
                          'plan_features': get_plan_features(company.id)
                      })
    except (Company.DoesNotExist, Embed.DoesNotExist):
        raise Http404
