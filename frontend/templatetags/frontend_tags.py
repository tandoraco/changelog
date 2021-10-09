from html.parser import HTMLParser

from django import template
from django.template.defaultfilters import stringfilter

from frontend.views.integrations import INTEGRATION_FRONTEND_META_DICT

register = template.Library()

class HTML2Text(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


@register.simple_tag(takes_context=True)
def public_page_url(context):
    request = context['request']
    return request.session["public-page-url"]


@register.filter
@stringfilter
def extract_text_and_truncate(value):
    html_2_text = HTML2Text()
    html_2_text.feed(value)
    return html_2_text.text.strip()[:30]


@register.filter
def meta_description(value):
    html_2_text = HTML2Text()
    html_2_text.feed(value)
    return html_2_text.text.strip()[:300]


@register.filter
@stringfilter
def get_integration_meta(value, arg):
    return INTEGRATION_FRONTEND_META_DICT[arg][value]


@register.filter
@stringfilter
def ul_list(value):
    ul = '<ul>'
    for val in value.split('.'):
        if val:
            ul += f'<li>{val}.</li>'
    ul += '</ul>'
    return ul


@register.filter
@stringfilter
def replace_changelog_with_page(value):
    if 'Changelog' in value:
        value = value.replace('Changelog', 'Page')
    if 'changelog' in value:
        value = value.replace('changelog', 'page')
    return value
