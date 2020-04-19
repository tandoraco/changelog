import pytest

from v1.settings.public_page.models import PublicPage
from v1.settings.public_page.views import PublicPageViewSet
from v1.utils.test_base.integration_test_base import ModelViewSetTestBase, CREATE, GET, DELETE


@pytest.mark.integration
class TestPublicPageViewSet(ModelViewSetTestBase):
    viewset = PublicPageViewSet
    url = "/api/v1/settings/public-page/"

    def test_not_allowed_method(self, user):
        not_allowed_methods = [CREATE, GET, DELETE]
        self.run_not_allowed_methods_assertions(user, not_allowed_methods=not_allowed_methods)

    def test_allowed_methods(self, user, public_page):
        self.queryset = PublicPage.objects.all()
        keys = [
            "hide_from_crawlers",
        ]
        self.run_assertions_for_retrieve(user, keys=keys)

        update_data = {
            "valid_data": {"banner_color": "#000000"},
            "invalid_data": {"banner_color": "asdnbfd"}
        }
        self.run_assertions_for_partial_update(user, update_data=update_data)
