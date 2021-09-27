import pytest
from django.urls import reverse
from rest_framework import status

from frontend.custom.test_utils import TandoraTestClient


@pytest.mark.django_db
class TestWidgetViews:
    client = TandoraTestClient()

    @pytest.mark.django_db
    def test_manage_widget_view(self, company, active_user, widget):
        if company.is_trial_account:
            company.is_trial_account = False
            company.save()

        url = reverse('frontend-manage-widget')

        # did not login, should redirect to login page
        response = self.client.get(url)
        assert 'login' in response.url
        assert 'redirect_to' in response.url
        assert url in response.url

        self.client.force_login(active_user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_public_widget_view_when_widget_disabled(self, company, user, widget):
        assert not widget.enabled

        # if widget is not enabled, public widget page should return 404
        url = self.client.get_public_widget_url(company)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_public_widget_view_when_widget_enabled(self, company, user, widget):
        company.use_case = 'c'
        company.save()
        widget.enabled = True
        widget.save()
        widget.refresh_from_db()

        response = self.client.get(self.client.get_public_widget_url(company))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_manage_widget_shows_widget_create_form_when_company_has_no_widget(self, company, active_user):
        url = reverse('frontend-manage-widget')
        self.client.force_login(active_user)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode('utf-8').lower()
        response_content = response_content.lower()
        assert 'create' in response_content
        assert 'embed' in response_content

    @pytest.mark.django_db
    def test_manage_widget_shows_widget_edit_form_when_company_has_widget(self, company, active_user, widget):
        url = reverse('frontend-manage-widget')
        self.client.force_login(active_user)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode('utf-8')
        response_content = response_content.lower()
        assert 'edit' in response_content.lower()
        assert 'embed' in response_content
