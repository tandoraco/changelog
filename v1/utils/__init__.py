import json

from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
from rest_framework import status
from rest_framework.response import Response


def serializer_error_response(serializer):
    return Response(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        data=serializer.errors)


def unprocessable_entity(detail):
    return Response(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        data={
            'detail': detail
        }
    )


def prettify_json(data):
    if isinstance(data, str):
        data = json.loads(data)
    data = json.dumps(data, indent=2)

    formatter = HtmlFormatter(style='colorful')
    response = highlight(data, JsonLexer(), formatter)

    style = f'<style>{formatter.get_style_defs()}+</style></br>'

    return mark_safe(f'{style}{response}')
