import json
import uuid
from html.parser import HTMLParser

import requests
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
from rest_framework import status
from rest_framework.response import Response

SLACK_URL = "https://hooks.slack.com/services/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"


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


def random_uuid():
    return str(uuid.uuid4())


def send_to_slack(message):
    data = {
        'text': '@channel ' + message
    }
    requests.post(SLACK_URL, json=data)


def html_2_text(html):

    class HTML2TextParser(HTMLParser):
        text = ""

        def handle_data(self, data):
            self.text += data

    html_parser = HTML2TextParser()
    html_parser.feed(html)

    return html_parser.text


def extract_all_image_src_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    return [img_tag['src'] for img_tag in img_tags]
