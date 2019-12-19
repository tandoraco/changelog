import pytest
from django.urls import reverse
from rest_framework import status

from frontend.custom.test_utils import TandoraTestClient


@pytest.mark.django_db
class TestFrontendStaticViews:
    client = TandoraTestClient()

    def test_static_site_not_allowed_when_company_use_case_is_changelog(self, company, user, widget):
        assert company.use_case == 'c'

        # When company use case is changelog, static site is not allowed
        url = reverse('frontend-manage-static-site')
        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url != url
        assert response.url == '/staff/changelogs'

    def test_404_when_static_site_is_not_configured(self, company):
        company.use_case = 's'
        company.save()
        company.refresh_from_db()

        url = self.client.get_public_page_url(company)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_custom_static_site_is_rendered_when_config_is_present(self, company,
                                                                   theme,
                                                                   static_site_field_values,
                                                                   static_site_config):
        url = self.client.get_public_page_url(company)

        assert company.theme
        assert company.settings['static_site_config']

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response_content = response.content.decode()
        for field_name, field_value in static_site_field_values.items():
            assert field_name in response_content
