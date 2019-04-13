import pytest

from v1.categories.models import Category
from v1.categories.views import CategorySerializer


@pytest.fixture
def category_data():
    data = []
    data.append({'name': 'New feature', 'color': '#FF0000'})
    data.append({'name': 'Bugfix', 'color': '#00FF00'})
    data.append({'name': 'Enhancement', 'color': '#0000FF'})

    return data


@pytest.fixture
def categories(category_data):
    for category in category_data:
        serializer = CategorySerializer(data=category)
        if serializer.is_valid():
            serializer.save()

    return Category.objects.all()
