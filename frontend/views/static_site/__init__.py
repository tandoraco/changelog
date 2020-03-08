from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from frontend.constants import STATIC_SITE_CONFIGURE_SUCCESS, THEME_SET_SUCCESS
from frontend.custom.decorators import is_authenticated, requires_static_site
from frontend.custom.utils import get_company_from_request
from frontend.forms.static_site import StaticSiteForm, DefaultStaticSiteForm, ThemeForm
from v1.static_site.models import StaticSiteTheme


@is_authenticated
@requires_static_site
def static_site_form(request):
    company = get_company_from_request(request)

    meta = company.theme_meta()
    if meta['theme_type'].lower() == 'default':
        form = DefaultStaticSiteForm()
        if request.method == "POST":
            form = DefaultStaticSiteForm(data=request.POST)
    else:
        form = StaticSiteForm(fields=meta['fields'])
        if request.method == "POST":
            form = StaticSiteForm(fields=meta['fields'], data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            settings = company.settings
            settings['static_site_config'] = form.cleaned_data
            company.settings = settings
            company.save()
            messages.success(request, STATIC_SITE_CONFIGURE_SUCCESS)
            if request.session.get('setup-stage-redirection'):
                return HttpResponseRedirect(request.session['setup-stage-redirection'])
            else:
                return HttpResponseRedirect('/')
    else:
        if company.settings.get('static_site_config'):
            for setting_name, setting_value in company.settings['static_site_config'].items():
                if setting_name in form.fields:
                    form.fields[setting_name].initial = setting_value

    return render(request, 'staff/form.html', {
        'form': form,
        'title': 'Configure Website'
    })


@is_authenticated
@requires_static_site
def theme_form(request):
    company = get_company_from_request(request)

    form = ThemeForm(company=company)
    if request.method == "GET" and company.theme:
        form.fields['theme'].initial = StaticSiteTheme.objects.get(name__iexact=company.theme)
        print(form.fields['theme'].initial)

    if request.method == "POST":
        form = ThemeForm(company=company, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, THEME_SET_SUCCESS)
            if request.session.get('setup-stage-redirection'):
                return HttpResponseRedirect(request.session['setup-stage-redirection'])
            else:
                return HttpResponseRedirect('/')

    return render(request, 'staff/form.html', {
        'form': form,
        'title': 'Set Website Theme'
    })
