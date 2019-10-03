from django.http import Http404
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from frontend.constants import (WIDGET_DOES_NOT_EXIST,
                                WIDGET_CREATED_OR_EDITED_SUCCESSFULLY,
                                WIDGET_CODE_EDIT_WARNING)
from frontend.custom.decorators import is_authenticated
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import get_company_from_slug_and_changelog_terminology
from frontend.forms.widget import WidgetForm
from v1.accounts.models import Company
from v1.core.models import Changelog
from v1.widget.models import Embed


@is_authenticated
def widget_form(request):
    company_id = request.session['company-id']

    if Embed.objects.filter(company__id=company_id).count() == 0:
        action = 'create'
        initial = {
            'javascript': f'<script>\n /* {WIDGET_CODE_EDIT_WARNING} */ \n // Insert your code below \n </script>',
            'css': '{}'
        }
        id = None
    else:
        action = 'edit'
        initial = None
        id = Embed.objects.get(company__id=company_id).id

    return TandoraForm(Embed, WidgetForm, action, 'generic-after-login-form.html',
                       '/', initial=initial) \
        .get_form(request, success_message=WIDGET_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=WIDGET_DOES_NOT_EXIST, id=id)


@csrf_exempt
@xframe_options_exempt
def public_widget(request, company, changelog_terminology):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        widget = Embed.objects.get(company=company, enabled=True)
        changelogs = Changelog.objects.filter(company=company, published=True, deleted=False)[:10]
        return render(request, 'public-widget.html',
                      context={
                          'company': company,
                          'widget': widget,
                          'changelogs': changelogs
                      })
    except (Company.DoesNotExist, Embed.DoesNotExist):
        raise Http404
