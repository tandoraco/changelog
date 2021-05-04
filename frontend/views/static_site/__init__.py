from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from frontend.constants import STATIC_SITE_CONFIGURE_SUCCESS, THEME_SET_SUCCESS, \
    WEB_BUILDER_SETUP_COMPLETED_PREVIEW_WEBSITE_MESSAGE
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

    return render(request, 'staff/signup.html', {
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

    if request.method == "POST":
        form = ThemeForm(company=company, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, THEME_SET_SUCCESS)
            if request.session.get('setup-stage-redirection'):
                return HttpResponseRedirect(request.session['setup-stage-redirection'])
            else:
                return HttpResponseRedirect('/')

    return render(request, 'staff/signup.html', {
        'form': form,
        'title': 'Set Website Theme'
    })


@is_authenticated
@requires_static_site
def setup_web_builder(request, stage_id):
    web_builder_setup_stages = {
        1: reverse('frontend-manage-theme'),
        2: reverse('frontend-manage-static-site'),
        3: reverse('frontend-staff-index')
    }
    stage_info_messages = {
        1: 'Setup website: <br> Step 1/2: Choose a theme for your website',
        2: 'Setup website: <br> Step 2/2: Add data for your website.'
    }
    try:
        current_stage_view = web_builder_setup_stages[stage_id]

        if stage_id < len(web_builder_setup_stages):
            messages.info(request, message=stage_info_messages[stage_id])
            next_stage_id = stage_id + 1
            request.session['setup-stage-redirection'] = reverse('frontend-setup-web-builder', args=(next_stage_id, ))
        else:
            request.session.pop('setup-stage-redirection', None)
            messages.success(request,
                             message=WEB_BUILDER_SETUP_COMPLETED_PREVIEW_WEBSITE_MESSAGE.replace(
                                 'url', request.session['public-page-url']))
            with transaction.atomic():
                company = request.user.company
                settings = company.settings
                settings['is_first_login'] = False
                company.settings = settings
                company.save()

        return HttpResponseRedirect(current_stage_view)
    except (KeyError, ValueError):
        raise Http404
