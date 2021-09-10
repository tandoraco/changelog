from html import unescape

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, RequestContext

from frontend.forms.auth.utils import get_plan_features
from v1.settings.public_page.models import PublicPage


def get_context_and_template_name(company, changelog=False):
    template = 'public_v3/index.html' if not changelog else 'public_v3/changelog.html'
    context = {
        'company': company,
        'company_name': company.company_name,
        'terminology': company.changelog_terminology,
        'hide_tandora_logo': True
    }

    context.update({'plan_features': get_plan_features(company.id, company=company)})
    try:
        banner_title = company.publicpage.banner_title or company.company_name.title()
        banner_tagline = company.publicpage.banner_tag_line or company.changelog_terminology.title()
        context.update({
            'banner_title': banner_title,
            'banner_tagline': banner_tagline
        })
    except PublicPage.DoesNotExist:
        context.update({
            'banner_title': company.company_name.title(),
            'banner_tagline': company.changelog_terminology.title()
        })

    return context, template


def render_html_from_string(request, template_string, context):
    style = '''
    <style>
        .footer-tandora-branding {
            margin-top: auto;
            bottom: 0px;
            width: 100%;
            text-align: center;
            background: #FAFAFA;
            padding: 20px;
        }
    </style>
    '''
    tandora_branding = '''
    {% if plan_features.show_tandora_branding_at_footer %}
    <script>
        var footer = document.getElementsByTagName("footer");
        footerText = '';
        {% if plan_features.custom_footer_text %}
            footerText += '{{ plan_features.custom_footer_text }}'
        {% endif %}
        if(footer && footer.length == 1) {
            footer = footer[0];
            var tandoraBranding = document.createElement('div');
            tandoraBranding.classList.add('footer-tandora-branding')
            tandoraBranding.innerHTML = footerText +
            'Powered by <a target="_blank" href="https://tandora.co/?from=cweb-builder">Tandora</a>';
            footer.append(tandoraBranding);
        } else {
            footer = document.createElement('footer');
            footer.classList.add('footer-tandora-branding');
            footer.innerHTML = footerText +
            'Powered by <a target="_blank" href="https://tandora.co/?from=cweb-builder">Tandora</a>';
            document.body.append(footer);
        }
        </script>
    {% endif %}
    '''
    template_string = template_string.replace('</head>', style + '\n</head>')
    template_string = template_string.replace('</body>', tandora_branding + '\n</body>')
    template = Template(template_string)
    request_context = RequestContext(request, context)
    html = unescape(template.render(request_context))
    return HttpResponse(html, content_type='text/html')


def render_html_string_without_context(template_string):
    template = Template(template_string)
    return HttpResponse(template, content_type='text/html')


def render_custom_theme(company, context, request):
    theme_meta = company.theme_meta(return_fields=False)

    if theme_meta['theme_type'] == 'default' or theme_meta['theme_type'] == 'file':
        return render(request, theme_meta['theme'], context)
    else:
        return render_html_from_string(request, theme_meta['theme'], context)
