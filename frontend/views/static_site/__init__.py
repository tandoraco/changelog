from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from frontend.constants import STATIC_SITE_CONFIGURE_SUCCESS, NOT_ALLOWED
from frontend.custom.decorators import is_authenticated
from frontend.forms.static_site import StaticSiteForm
from v1.accounts.models import Company


@is_authenticated
def static_site_form(request):
    company_id = request.session['company-id']

    company = Company.objects.get(id=company_id)
    if not company.is_static_site:
        messages.info(request, NOT_ALLOWED)
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = StaticSiteForm(data=request.POST)
        if form.is_valid():
            settings = company.settings
            settings['static_site_config'] = form.cleaned_data
            company.settings = settings
            company.save()
            messages.success(request, STATIC_SITE_CONFIGURE_SUCCESS)
            return HttpResponseRedirect('/')
    else:
        form = StaticSiteForm()
        if company.settings.get('static_site_config'):
            for setting_name, setting_value in company.settings['static_site_config'].items():
                if setting_name in form.fields:
                    form.fields[setting_name].initial = setting_value

    return render(request, 'staff/form.html', {
        'form': form,
        'title': 'Configure static site'
    })
