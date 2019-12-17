import pytest
from django.urls import reverse
from rest_framework import status

from frontend.constants import NOT_ALLOWED
from frontend.custom.test_utils import TandoraTestClient
from frontend.forms.widget import WidgetForm


@pytest.mark.django_db
class TestWidgetViews:
    client = TandoraTestClient()

    def get_public_widget_url(self, company):
        return f'/{company.company_name}/{company.changelog_terminology}/widget/1'

    def test_manage_widget_view(self, company, user, widget):
        if company.is_trial_account:
            company.is_trial_account = False
            company.save()

        url = reverse('frontend-manage-widget')

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

    def test_widget_not_allowed_when_static_site_is_enabled(self, company, user, widget):
        assert company.use_case == 'c'
        company.use_case = 's'
        company.save()
        company.refresh_from_db()

        # When static site is enabled, we will redirect to /staff/changelogs page
        # with not allowed message.
        url = reverse('frontend-manage-widget')
        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url != url
        assert response.url == '/staff/changelogs'

    def test_manage_widget_shows_widget_create_form_when_company_has_no_widget(self, company, user):
        url = reverse('frontend-manage-widget')
        self.client.force_login(user)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode('utf-8')
        assert 'create embed' in response_content.lower()

    def test_manage_widget_shows_widget_edit_form_when_company_has_widget(self, company, user, widget):
        url = reverse('frontend-manage-widget')
        self.client.force_login(user)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode('utf-8')
        assert 'edit embed' in response_content.lower()
