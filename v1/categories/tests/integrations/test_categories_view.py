import random

import pytest
from faker import Faker
from rest_framework.test import (APIRequestFactory, force_authenticate)

from v1.categories.models import Category
from v1.categories.views import CategoriesViewset

factory = APIRequestFactory()
fake = Faker()


@pytest.mark.django_db
def test_categories_viewset_get(categories, user):
    view = CategoriesViewset.as_view({'get': 'list'})
    request = factory.get('/api/v1/categories/')
    response = view(request)
    assert response.status_code == 401

    force_authenticate(request, user)
    response = view(request)
    assert response.status_code == 200
    assert response.data
    assert len(response.data) == len(categories)
    response_data_keys = response.data[0].keys()
    assert "name" in response_data_keys
    assert "id" in response_data_keys
    assert "color" in response_data_keys

    category = random.choice(categories)
    view = CategoriesViewset.as_view({'get': 'retrieve'})
    response = view(request, pk=category.pk)
    assert response.status_code == 200
    assert response.data
    response_data = response.data
    assert response_data['id'] == category.id
    assert response_data['color'] == category.color
    assert response_data['name'] == category.name


@pytest.mark.django_db
def test_categories_viewset_create(user, category_data):
    view = CategoriesViewset.as_view({'post': 'create'})
    data = random.choice(category_data)
    request = factory.post('/api/v1/categories/', data)
    response = view(request)
    assert response.status_code == 401

    force_authenticate(request, user)
    response = view(request)
    assert response.status_code == 201
    assert response.data
    response_data = response.data
    assert data['name'] == response_data['name']
    assert data['color'] == response_data['color']

    data['color'] = "1234566"  # invalid color -> throw 422 and duplicate category
    request = factory.post('/api/v1/categories/', data)
    force_authenticate(request, user)
    response = view(request)
    assert response.status_code == 422

    data['name'] = "test"  # new category, invalid color
    request = factory.post('/api/v1/categories/', data)
    force_authenticate(request, user)
    response = view(request)
    assert response.status_code == 422


@pytest.mark.django_db
def test_categories_viewset_update(user, category_data, categories):
    view = CategoriesViewset.as_view({'patch': 'update'})
    data = random.choice(categories)
    request = factory.patch('/api/v1/categories/')
    response = view(request, pk=data.pk)
    assert response.status_code == 401

    patch_data = category_data[data.pk - 1]
    new_name = fake.name()
    patch_data['name'] = new_name
    request = factory.patch('/api/v1/categories/', data=patch_data)
    force_authenticate(request, user)
    response = view(request, pk=data.pk)
    assert response.status_code == 200
    assert response.data
    assert response.data['name'] == new_name

    new_name = new_name * 20  # category name can be atmost 50 characters
    patch_data['name'] = new_name
    request = factory.patch('/api/v1/categories/', data=patch_data)
    force_authenticate(request, user)
    response = view(request, pk=data.pk)
    assert response.status_code == 422
    assert "name" in response.data


@pytest.mark.django_db
def test_categories_viewset_delete(user, categories):
    view = CategoriesViewset.as_view({'delete': 'destroy'})
    data = random.choice(categories)
    request = factory.delete('/api/v1/categories/')
    response = view(request, pk=data.pk)
    assert response.status_code == 401

    force_authenticate(request, user)
    response = view(request, pk=data.pk)
    assert response.status_code == 204

    response = view(request, pk=data.pk)
    assert response.status_code == 404

    with pytest.raises(Category.DoesNotExist):
        Category.objects.get(pk=data.pk)
