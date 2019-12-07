from html.parser import HTMLParser

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag(takes_context=True)
def public_page_url(context):
    request = context['request']
    return request.session["public-page-url"]


@register.filter
@stringfilter
def extract_text_and_truncate(value):

    class HTML2Text(HTMLParser):
        text = ""

        def handle_data(self, data):
            self.text += data

    html_2_text = HTML2Text()
    html_2_text.feed(value)

    return html_2_text.text.strip()[:280]
