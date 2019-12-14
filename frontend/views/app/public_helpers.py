import datetime
from html import unescape

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import Template, RequestContext

from frontend.forms.static_site import FONT_CHOICES


def get_context_and_template_name(company, changelog=False):
    if company.is_static_site:
        template = 'public/static-site.html'

        try:
            config = company.settings['static_site_config']
        except KeyError:
            raise Http404

        font_name = ''
        for font_link, font in FONT_CHOICES:
            if config['font'] == font_link:
                font_name = font

        context = {
            'config': config,
            'company': company,
            'year': datetime.datetime.now().year,
            'font_name': font_name
        }
    else:
        template = 'public/index.html' if not changelog else 'public/changelog.html'
        context = {
            'company_name': company.company_name,
            'terminology': company.changelog_terminology,
            'hide_tandora_logo': True
        }

    return context, template


def render_html_from_string(request, template_string, context):
    template = Template(template_string)
    request_context = RequestContext(request, context)
    html = unescape(template.render(request_context))
    return HttpResponse(html, content_type='text/html')


def render_custom_theme(company, context, request):
    theme_meta = company.theme_meta(return_fields=False)

    if theme_meta['theme_type'] == 'default' or theme_meta['theme_type'] == 'file':
        return render(request, theme_meta['theme'], context)
    else:
        return render_html_from_string(request, theme_meta['theme'], context)
