from importlib import import_module

from django.conf import settings
from django.http import HttpRequest
from django.test import Client

from frontend.forms.auth.utils import create_session


class TandoraTestClient(Client):

    def force_login(self, user, backend=None):
        # Took this code from Client.force_login and modified to use our create_session
        # Create a fake request to store login details.
        engine = import_module(settings.SESSION_ENGINE)

        # Create a fake request to store login details.
        request = HttpRequest()

        if self.session:
            request.session = self.session
        else:
            request.session = engine.SessionStore()
        # our app create session
        create_session(user.email, request)

        # Save the session values.
        request.session.save()

        # Set the cookie to represent the session.
        session_cookie = settings.SESSION_COOKIE_NAME
        self.cookies[session_cookie] = request.session.session_key
        cookie_data = {
            'max-age': None,
            'path': '/',
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'expires': None,
        }
        self.cookies[session_cookie].update(cookie_data)
