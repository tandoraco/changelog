import random

import pytest
from django.contrib.messages import get_messages
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status

from frontend.constants import PLAN_LIMIT_REACHED_MESSAGE
from frontend.custom.test_utils import FrontEndFormViewTestBase, test_url
from frontend.forms.auth.utils import DEFAULT_PLAN_FEATURES
from v1.categories.constants import DELETED_CATEGORY
from v1.categories.models import Category

VIEW_CATEGORIES = 'frontend-view-categories'
CREATE_CATEGORY = 'frontend-create-category'
EDIT_CATEGORY = 'frontend-edit-category'
DELETE_CATEGORY = 'frontend-delete-category'


@pytest.mark.django_db
class TestFrontEndCategoryViews:

    def test_category_frontend_views(self, active_user, company, categories, category):
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
            user=active_user,
            company=company,
            queryset=categories,
            instance=category
        )

    def test_frontend_create_category(self, active_user, category_data):
        url = reverse('frontend-create-category')

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(active_user)

        for data in category_data:
            client.post(url, data=data)

        assert Category.objects.count() == len(category_data)

    def test_frontend_update_category(self, active_user, category, categories):
        url = reverse('frontend-edit-category', kwargs={'id': category.id})

        old_category_name = category.name
        new_category_name = 'Test123'
        data = model_to_dict(category)
        data['name'] = new_category_name

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(active_user)

        client.post(url, data=data)

        category.refresh_from_db()
        assert category.name == new_category_name
        assert category.name != old_category_name

        url = reverse('frontend-edit-category', kwargs={'id': 100})
        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_plan_limits(self, active_user):
        # Default category limit is 5
        category_names = [
            'Test 1',
            'Test 2',
            'Test 3',
            'Test 4',
            'Test 5',
            'Test 6',
        ]
        colors = [
            '#000001',
            '#000002',
            '#000003',
            '#000004',
            '#000005',
            '#000006',
        ]

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(active_user)
        url = reverse('frontend-create-category')

        for i in range(DEFAULT_PLAN_FEATURES['categories']):
            data = {
                'name': category_names[i],
                'color': colors[i]
            }
            response = client.post(url, data=data)
            client.assert_response_message_icontains(response, 'successfully create category')

        data = {
            'name': category_names[-1],
            'color': colors[-1]
        }
        response = client.post(url, data=data)
        client.assert_response_message(response, PLAN_LIMIT_REACHED_MESSAGE)
