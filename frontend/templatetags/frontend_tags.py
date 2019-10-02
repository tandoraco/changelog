from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def public_page_url(context):
    request = context['request']
    return request.session["public-page-url"]
