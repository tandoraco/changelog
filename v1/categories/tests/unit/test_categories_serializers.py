import pytest

from v1.categories.serializers import CategorySerializer
from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase


@pytest.mark.django_db
class TestCategoriesSerializer(SerializerTestBase):
    serializer_class = CategorySerializer

    def test_data(self):
        data = []
        data.append(SerializerTestData(data={'name': 'Hello', 'color': '#123456'}, is_valid=True))
        data.append(SerializerTestData(data={'name': 'New', 'color': 'ASRERDF3'},
                                       is_valid=False))  # color code more than 7 characters
        data.append(SerializerTestData(data={'name': 'New', 'color': '#ASRERD'}, is_valid=False))  # hex code is invalid
        data.append(SerializerTestData(data={'name': 'NEW', 'color': '#123456'},
                                       is_valid=True))  # Category name is already present, category names are case insensitive
        data.append(SerializerTestData(data={'name': 'Yes', 'color': '#ASRERD'}, is_valid=False))  # Invalid hex code
        data.append(SerializerTestData(data={'name': 'Yes', 'color': '#00FF00'}, is_valid=True))
        data.append(SerializerTestData(data={'name': 'Yes', 'color': '#00FF00'}, is_valid=False))  # Duplicate entry

        self.run_data_assertions(data, create_db_entry=True)
