import pytest
from django.urls import reverse
from rest_framework import status

from frontend.custom.test_utils import TandoraTestClient

VIEW_CATEGORIES = 'frontend-view-categories'
CREATE_CATEGORY = 'frontend-create-category'
EDIT_CATEGORY = 'frontend-edit-category'
DELETE_CATEGORY = 'frontend-delete-category'


@pytest.mark.django_db
class TestFrontEndCategoryViews:
    client = TandoraTestClient()

    def test_view_categories(self, company, user, categories):
        url = reverse(VIEW_CATEGORIES)
        self.client.force_login(user)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode()
        for category in categories:
            assert category.name in response_content

    def test_delete_category(self, company, user, category):
        assert not category.deleted

        url = reverse(DELETE_CATEGORY, kwargs={'id': category.id})
        self.client.force_login(user)
        response = self.client.get(url)
        # on success we will be redirected to some other page
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse(VIEW_CATEGORIES)

        category.refresh_from_db()
        assert category.deleted

        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_create_category(self, company, user):
        url = reverse(CREATE_CATEGORY)
        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode().lower()
        assert 'create category' in response_content

    def test_edit_category(self, company, user, category):
        url = reverse(EDIT_CATEGORY, kwargs={'id': category.id})
        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode().lower()
        assert 'edit category' in response_content
        assert category.name.lower() in response_content
        assert category.color.lower() in response_content

        # deleted category editing should return 404
        category.deleted = True
        category.save()
        category.refresh_from_db()
        url = reverse(EDIT_CATEGORY, kwargs={'id': category.id})
        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # unexisting category editing should return 404
        url = reverse(EDIT_CATEGORY, kwargs={'id': 100})
        self.client.force_login(user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
