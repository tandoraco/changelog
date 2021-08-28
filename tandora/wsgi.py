"""
WSGI config for tandora project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from dj_static import Cling
from django.core.wsgi import get_wsgi_application
import newrelic.agent
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tandora.settings')

if os.environ.get('DEBUG'):
    application = Cling(get_wsgi_application())
else:
    application = Cling(get_wsgi_application())
