import pytest
from django.urls import reverse
from rest_framework import status

from frontend.custom.test_utils import TandoraTestClient


@pytest.mark.django_db
class TestFrontendStaticViews:
    client = TandoraTestClient()

    @pytest.mark.django_db
    def test_static_site_not_allowed_when_company_use_case_is_changelog(self, company, active_user, widget):
        assert company.use_case == 'c'

        # When company use case is changelog, static site is not allowed
        url = reverse('frontend-manage-static-site')
        self.client.force_login(active_user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url != url
        assert response.url == '/staff'

    @pytest.mark.django_db
    def test_404_when_static_site_is_not_configured(self, company):
        company.use_case = 's'
        company.save()
        company.refresh_from_db()

        url = self.client.get_public_page_url(company)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_custom_static_site_is_rendered_when_config_is_present(self, company,
                                                                   theme,
                                                                   static_site_field_values,
                                                                   static_site_config):
        url = self.client.get_public_page_url(company)

        assert company.theme
        assert company.settings['static_site_config']

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # response_content = response.content.decode()
        # for field_name, field_value in static_site_field_values.items():
        #     if field_name != 'font':
        #         assert field_name in response_content

    @pytest.mark.django_db
    def test_company_name_alone_in_url_redirects_to_public_company_index(self, company):
        url = f'/{company.company_name.lower()}'

        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response['Location'].lower() == f'/{company.company_name}/{company.changelog_terminology}'.lower().replace(' ', '-')

    @pytest.mark.django_db
    def test_manage_widget_not_present_for_tandora_web_builder_product(self, company, active_user):
        company.use_case = 's'
        company.save()
        url = reverse('frontend-staff-index')
        self.client.force_login(active_user)

        response = self.client.get(url)
        response_content = response.content.decode()

        assert reverse('frontend-manage-widget') not in response_content
        assert reverse('frontend-manage-theme') in response_content
        assert reverse('frontend-manage-static-site') in response_content

    @pytest.mark.django_db
    def test_manage_static_site_is_not_in_tandora_changelog_product(self, company, active_user):
        assert company.use_case == 'c'

        url = reverse('frontend-staff-index')
        self.client.force_login(active_user)

        response = self.client.get(url)
        response_content = response.content.decode()

        assert reverse('frontend-manage-widget') in response_content
        assert reverse('frontend-manage-theme') not in response_content
        assert reverse('frontend-manage-static-site') not in response_content

    @pytest.mark.django_db
    def test_web_builder_setup_at_first_login(self, company, active_user, user_data):
        assert company.is_first_login
        company.use_case = 's'
        company.save()

        data = {
            'email': active_user.email,
            'password': user_data['password']
        }

        url = reverse('frontend-login')
        response = self.client.post(url, data=data)
        # on successful first login for web builder page , we will show web builder setup
        assert response.status_code == status.HTTP_302_FOUND
        assert 'setup/stage/1' in response.url

        settings = company.settings
        settings['is_first_login'] = False
        company.settings = settings
        company.save()

        url = reverse('frontend-login')
        response = self.client.post(url, data=data)
        # once we disable is_first_login, successful login will redirect to staff index page
        assert response.status_code == status.HTTP_302_FOUND
        assert 'setup/stage/1' not in response.url

    @pytest.mark.django_db
    def test_web_builder_setup_stage_1(self, static_site_company, active_user, user_data):
        assert static_site_company.is_first_login
        stage_1 = 1
        url = reverse('frontend-setup-web-builder', args=(stage_1, ))
        self.client.force_login(active_user)

        response = self.client.get(url)
        assert response.url == reverse('frontend-manage-theme')

    @pytest.mark.django_db
    def test_web_builder_setup_stage_2(self, static_site_company, active_user, user_data):
        assert static_site_company.is_first_login
        stage_2 = 2
        url = reverse('frontend-setup-web-builder', args=(stage_2,))
        self.client.force_login(active_user)

        response = self.client.get(url)
        assert response.url == reverse('frontend-manage-static-site')

    @pytest.mark.django_db
    def test_web_builder_setup_stage_3(self, static_site_company, active_user, user_data):
        assert static_site_company.is_first_login

        stage_3 = 3
        url = reverse('frontend-setup-web-builder', args=(stage_3,))
        self.client.force_login(active_user)

        response = self.client.get(url)
        assert response.url == reverse('frontend-staff-index')

        static_site_company.refresh_from_db()
        # We currently have 3 stages in web builder setup
        # The last stage is stage 3, which just shows success message
        # On this stage, we mark the is_first_login as false, so setup won't be shown
        assert not static_site_company.is_first_login
