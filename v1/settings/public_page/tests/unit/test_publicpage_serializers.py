import pytest

from v1.settings.public_page.models import PublicPage
from v1.settings.public_page.serializers import PublicPageSerializer
from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase


@pytest.mark.unit
class TestPublicPageSerializer(SerializerTestBase):
    serializer_class = PublicPageSerializer

    def test_publicpage_serializer(self, company):
        data = []

        data.append(SerializerTestData(data={"color": "123"}, is_valid=False))
        data.append(SerializerTestData(data={"color": "qweert"}, is_valid=False))
        data.append(SerializerTestData(data={"color": "000033"}, is_valid=False))
        data.append(SerializerTestData(data={"company": company.id, "color": "#000033"}, is_valid=True))

        self.run_data_assertions(test_data=data)

    def test_publicpage_serializer_with_create_db_entry_defaults(self, company):
        data = []

        color = "123"
        data.append(SerializerTestData(data={"company": company.id, "color": color}, is_valid=True))
        self.run_data_assertions(test_data=data, create_db_entry=True)

        public_page = PublicPage.objects.get(company=company)
        assert public_page.color == color
        # they fall back to defaults, if no values are provided
        assert not public_page.hide_from_crawlers
        assert not public_page.show_authors
        assert not public_page.private_mode

    def test_publicpage_serializer_with_create_db_entry_defaults_non_default(self, company):
        data = []

        color = "123"
        data.append(
            SerializerTestData(data={
                "company": company.id,
                "color": color,
                "hide_from_crawlers": True,
                "private_mode": True
            }, is_valid=True))
        self.run_data_assertions(test_data=data, create_db_entry=True)

        public_page = PublicPage.objects.get(company=company)
        assert public_page.company.id == company.id
        assert public_page.color == color
        assert public_page.hide_from_crawlers
        assert not public_page.show_authors
        assert public_page.private_mode
