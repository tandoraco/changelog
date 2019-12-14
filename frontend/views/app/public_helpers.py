import datetime

from django.http import Http404

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
