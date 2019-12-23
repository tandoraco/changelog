import random
from collections import namedtuple
from importlib import import_module

import pytest
from django.conf import settings
from django.http import HttpRequest
from django.test import Client
from rest_framework import status

from frontend.forms.auth.utils import create_session

test_url = namedtuple('test_url', 'name url')


class TandoraTestClient(Client):

    def get_public_page_url(self, company):
        return f'/{company.company_name}/{company.changelog_terminology}'

    def get_public_widget_url(self, company):
        return f'{self.get_public_page_url(company)}/widget/1'

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


@pytest.mark.django_db
class FrontEndFormViewTestBase:

    def __init__(self, model_name, urls, fields, view_exclude_fields, user, company, queryset, instance):
        self.model_name = model_name
        self.urls = urls
        self.fields = fields
        self.client = TandoraTestClient()
        self.user = user
        self.company = company
        self.queryset = queryset  # Equivalent to model.objects.all()
        self.instance = instance  # stores a single model. Equivalent to model.objects.get()
        self.view_exclude_fields = view_exclude_fields
        self.run_tests()

    def restore_instance(self):
        # at the end of each test, un delete the instance if deleted
        if getattr(self.instance, 'deleted'):
            setattr(self.instance, 'deleted', False)
            self.instance.save()
            self.instance.refresh_from_db()

    def test_create(self, url):
        self.client.force_login(self.user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode().lower()
        assert f'create {self.model_name.lower()}' in response_content

    def test_edit(self, url):
        self.client.force_login(self.user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode()
        assert f'edit {self.model_name.lower()}' in response_content.lower()
        for field in self.fields:
            assert str(getattr(self.instance, field)) in response_content

        setattr(self.instance, 'deleted', True)
        self.instance.save()
        self.instance.refresh_from_db()
        self.client.force_login(self.user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # unexisting model editing should return 404
        url = url.replace(str(self.instance.id), str(random.randint(50, 100)))
        self.client.force_login(self.user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        self.restore_instance()

    def test_delete(self, url):
        assert not self.instance.deleted

        self.client.force_login(self.user)
        response = self.client.get(url)
        # on success we will be redirected to some other page
        assert response.status_code == status.HTTP_302_FOUND

        self.instance.refresh_from_db()
        assert self.instance.deleted

        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND

        self.restore_instance()

    def test_view(self, url):
        self.client.force_login(self.user)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode()
        for obj in self.queryset:
            for field in self.fields:
                if field not in self.view_exclude_fields:
                    assert getattr(obj, field) in response_content

    def run_tests(self):
        for url in self.urls:
            print(f'Running tests for {url.name} -> {self.model_name}')
            getattr(self, f'test_{url.name}')(url.url)
