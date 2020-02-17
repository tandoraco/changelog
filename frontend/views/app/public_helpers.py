import datetime
from html import unescape

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import Template, RequestContext

from frontend.forms.auth.utils import get_plan_features
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
            'title': company.publicpage.title,
            'tag_line': company.publicpage.tag_line,
            'font_link': company.publicpage.font,
            'font': company.publicpage.get_font_display(),
            'color': company.publicpage.color,
            'hide_tandora_logo': True,
        }

    context.update({'plan_features': get_plan_features(company.id)})

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
        if(footer && footer.length == 1) {
            footer = footer[0];
            var tandoraBranding = document.createElement('div');
            tandoraBranding.classList.add('footer-tandora-branding')
            tandoraBranding.innerHTML='Powered by <a href="https://www.tandora.co/?from=cweb-builder">Tandora</a>';
            footer.append(tandoraBranding);
        } else {
            footer = document.createElement('footer');
            footer.classList.add('footer-tandora-branding');
            footer.innerHTML = 'Powered by <a href="https://www.tandora.co/?from=cweb-builder">Tandora</a>';
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
