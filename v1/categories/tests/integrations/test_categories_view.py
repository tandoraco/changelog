import pytest
from faker import Faker

from v1.categories.models import Category
from v1.categories.views import CategoriesViewset
from v1.utils.test_base.integration_test_base import ModelViewsetTestBase


@pytest.mark.integration
class TestCategoriesViewset(ModelViewsetTestBase):
    viewset = CategoriesViewset
    url = "/api/v1/categories"
    model = Category

    def test_category_viewset(self, user, categories, category_data):
        self.queryset = categories
        fake = Faker()
        name = fake.name()

        create_data = dict()
        create_data["valid_data"] = {"name": name, "color": "#00ff00"}
        create_data["invalid_data"] = {"name": name, "color": "#00ff00"}

        update_data = dict()
        update_data["valid_data"] = {"name": fake.name()}
        update_data["invalid_data"] = {"color": "12345565"}

        keys = ["name", "color"]
        self.run_all_assertions(user, create_data, update_data, get_keys=keys)
