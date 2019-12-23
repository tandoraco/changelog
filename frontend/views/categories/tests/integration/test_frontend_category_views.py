import pytest
from django.urls import reverse

from frontend.custom.test_utils import FrontEndFormViewTestBase, test_url

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
