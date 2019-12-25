import random

import pytest
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status

from frontend.custom.test_utils import FrontEndFormViewTestBase, test_url
from v1.categories.constants import DELETED_CATEGORY
from v1.categories.models import Category

VIEW_CATEGORIES = 'frontend-view-categories'
CREATE_CATEGORY = 'frontend-create-category'
EDIT_CATEGORY = 'frontend-edit-category'
DELETE_CATEGORY = 'frontend-delete-category'


@pytest.mark.django_db
class TestFrontEndCategoryViews:

    def test_category_frontend_views(self, user, company, categories, category):
        urls = [
            test_url('create', reverse(CREATE_CATEGORY)),
            test_url('edit', reverse(EDIT_CATEGORY, kwargs={'id': category.id})),
            test_url('delete', reverse(DELETE_CATEGORY, kwargs={'id': category.id})),
            test_url('view', reverse(VIEW_CATEGORIES)),
        ]

        FrontEndFormViewTestBase(
            model_name='Category',
            urls=urls,
            fields=['name', 'color'],
            view_exclude_fields={'color'},
            user=user,
            company=company,
            queryset=categories,
            instance=category
        )

    def test_frontend_create_category(self, user, category_data):
        url = reverse('frontend-create-category')

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(user)

        for data in category_data:
            client.post(url, data=data)

        assert Category.objects.count() == len(category_data)

    def test_frontend_update_category(self, user, category, categories):
        url = reverse('frontend-edit-category', kwargs={'id': category.id})

        old_category_name = category.name
        new_category_name = 'Test123'
        data = model_to_dict(category)
        data['name'] = new_category_name

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(user)

        client.post(url, data=data)

        category.refresh_from_db()
        assert category.name == new_category_name
        assert category.name != old_category_name

        url = reverse('frontend-edit-category', kwargs={'id': 100})
        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
