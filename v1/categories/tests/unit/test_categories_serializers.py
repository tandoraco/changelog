import pytest

from v1.categories.constants import DELETED_CATEGORY
from v1.categories.serializers import CategorySerializer
from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase


@pytest.mark.django_db
@pytest.mark.unit
class TestCategoriesSerializer(SerializerTestBase):
    serializer_class = CategorySerializer

    def test_data(self, company):
        data = [
            # company not provided, so false data
            SerializerTestData(data={'name': 'Hello', 'color': '#123456'}, is_valid=False),
            # color not valid
            SerializerTestData(data={'company': company.id, 'name': 'New', 'color': 'ASRERDF3'},
                               is_valid=False),
            SerializerTestData(data={'company': company.id, 'name': 'New', 'color': '#ASRERD'}, is_valid=False),
            SerializerTestData(data={'company': company.id, 'name': 'NEW', 'color': '#123456'},
                               is_valid=True),
            SerializerTestData(data={'name': 'Yes', 'color': '#ASRERD'}, is_valid=False),
            SerializerTestData(data={'company': company.id, 'name': 'Yes', 'color': '#00FF00'}, is_valid=True),
            # category name exists so false data
            SerializerTestData(data={'company': company.id, 'name': 'Yes', 'color': '#00FF00'}, is_valid=False)
        ]

        self.run_data_assertions(data, create_db_entry=True)


@pytest.mark.unit
@pytest.mark.django_db
def test_cannot_create_category_with_deleted_category_name(company):
    data = {
        'name': 'test',
        'color': '#000000',
        'company': company.id
    }

    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()
    category = serializer.save()
    category.deleted = True
    category.save()

    data['color'] = '#FF0000'
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert str(serializer.errors['name'][0]) == DELETED_CATEGORY
