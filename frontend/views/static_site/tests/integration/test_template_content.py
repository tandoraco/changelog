import pytest
from django.urls import reverse

from frontend.custom.test_utils import TandoraTestClient


@pytest.mark.django_db
class TestTemplateContent:
    client = TandoraTestClient()
    url = reverse('frontend-staff-index')

    def _run_brand_test(self, user, product_name):
        self.client.force_login(user)
        response = self.client.get(self.url)

        response_content = response.content.decode()
        assert product_name in response_content

    @pytest.mark.django_db
    def test_brand_name_for_tandora_changelog_product(self, company, active_user):
        self._run_brand_test(active_user, 'Tandora Changelog')

    @pytest.mark.django_db
    def test_brand_name_for_tandora_web_builder_product(self, company, active_user):
        company.use_case = 's'
        company.save()
        self._run_brand_test(active_user, 'Tandora Web builder')
