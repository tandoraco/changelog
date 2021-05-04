from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from frontend.constants import (WIDGET_DOES_NOT_EXIST,
                                WIDGET_CREATED_OR_EDITED_SUCCESSFULLY,
                                WIDGET_CODE_EDIT_WARNING, NOT_ALLOWED)
from frontend.custom.decorators import is_authenticated
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import get_company_from_slug_and_changelog_terminology, get_public_changelog_limit
from frontend.forms.auth.utils import get_plan_features
from frontend.forms.widget import WidgetForm
from v1.accounts.models import Company
from v1.widget.models import Embed

INITIAL_JAVASCRIPT = f'<script>\n /* {WIDGET_CODE_EDIT_WARNING} */ \n // Insert your code below \n </script>'
INITIAL_CSS = '{}'


@is_authenticated
def widget_form(request):
    extra = None

    company = request.user.company
    if company.is_static_site:
        messages.info(request, NOT_ALLOWED)
        return HttpResponseRedirect('/staff')
    try:
        embed = company.embed
        embed_exists = True
    except Embed.DoesNotExist:
        embed = None
        embed_exists = False

    if not embed_exists:
        action = 'create'
        initial = {
            'javascript': INITIAL_JAVASCRIPT,
            'css': INITIAL_CSS
        }
    else:
        action = 'edit'
        initial = None

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
            public_page_url = reverse('frontend-public-widget', kwargs={'company': slugify(company.company_name)})
            extra = f'<i><a target="_blank" href="{public_page_url}">Click here</a> to view widget.</i>'

    return TandoraForm(Embed, WidgetForm, action, 'staff_v2/postlogin_form.html',
                       reverse('frontend-manage-widget'), initial=initial) \
        .get_form(request, instance=embed, success_message=WIDGET_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=WIDGET_DOES_NOT_EXIST, extra=extra)


def render_widget(request, company, changelog_terminology):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        widget = company.embed
        if not widget.enabled:
            raise Embed.DoesNotExist
        changelogs = company.changelog_set.filter(company=company,
                                                  published=True,
                                                  deleted=False).order_by('-created_at').select_related()[:10]

        return render(request, 'public/widget.html',
                      context={
                          'company': company,
                          'widget': widget,
                          'changelogs': changelogs,
                          'hide_tandora_logo': True,
                          'page_title': f'{str(company)} widget'.title(),
                          'plan_features': get_plan_features(company.id, company=company),
                          'changelog_limit': get_public_changelog_limit(company)
                      })
    except (Company.DoesNotExist, Embed.DoesNotExist, IndexError):
        raise Http404


@csrf_exempt
@xframe_options_exempt
def public_widget(request, company):
    return render_widget(request, company, None)


@csrf_exempt
@xframe_options_exempt
def legacy_widget(request, company, changelog_terminology):
    if company.lower() == 'vriksham-pre-pregnancy-classes' or company.lower() == 'doctorparoma':
        return render_widget(request, company, None)
    else:
        raise Http404
