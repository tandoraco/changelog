import mock
import pytest
from django.test import Client
from rest_framework import status

from frontend.custom.test_utils import TandoraTestClient


@pytest.mark.django_db
class TestWidgetViews:
    client = TandoraTestClient()

    def get_public_widget_url(self, company):
        return f'/{company.company_name}/{company.changelog_terminology}/widget/1'

    def test_manage_widget_view(self, company, user, widget):
        if company.is_trial_account:
            company.is_trial_account = False
            company.save()

        url = '/staff/manage/widget'

        # did not login, should redirect to login page
        response = self.client.get(url)
        assert 'login' in response.url
        assert 'redirect_to' in response.url
        assert url in response.url

        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_public_widget_view_when_widget_disabled(self, company, user, widget):
        assert not widget.enabled

        # if widget is not enabled, public widget page should return 404
        url = self.get_public_widget_url(company)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_public_widget_view_when_widget_enabled(self, company, user, widget):
        widget.enabled = True
        widget.save()
        widget.refresh_from_db()

        response = self.client.get(self.get_public_widget_url(company))
        assert response.status_code == status.HTTP_200_OK
