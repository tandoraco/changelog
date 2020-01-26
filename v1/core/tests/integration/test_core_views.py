import copy

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from v1.core.models import Changelog
from v1.core.views import ChangelogViewSet, inline_image_attachment
from v1.utils.test_base.integration_test_base import ModelViewSetTestBase


@pytest.mark.integration
class TestChangelogViewSet(ModelViewSetTestBase):
    viewset = ChangelogViewSet
    url = "/api/v1/changelogs"
    model = Changelog

    def test_changelog_views(self, changelog1_data, changelog2_data, admin, published_changelog, unpublished_changelog):
        self.queryset = Changelog.objects.all()

        create_data = dict()
        create_data["valid_data"] = changelog1_data
        invalid_data = copy.deepcopy(changelog2_data)
        invalid_data["title"] = "a" * 201  # title can be at most 200 chars
        create_data["invalid_data"] = invalid_data

        update_data = dict()
        update_data["valid_data"] = {"content": "We are starting a changelog. Watch this space."}
        update_data["invalid_data"] = {"category": 100}  # category does not exists

        keys = ["title", "content", "category", "created_by", "last_edited_by"]
        self.run_all_assertions(admin, create_data, update_data, get_keys=keys)


@pytest.mark.integration
@pytest.mark.django_db
def test_image_inline_attachment(company, image, text_file):
    url = reverse('v1-inline-image')
    factory = APIRequestFactory()

    data = {
        'file': image,
        'company': company.id
    }
    request = factory.post(url, data)
    setattr(request, 'session', {})
    response = inline_image_attachment(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    force_authenticate(request, user=company.admin)
    response = inline_image_attachment(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'location' in response.data

    data = {
        'file': image
    }
    request = factory.post(url, data)
    setattr(request, 'session', {})
    force_authenticate(request, user=company.admin)
    response = inline_image_attachment(request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = {
        'file': text_file,
        'company': company.id
    }
    request = factory.post(url, data)
    setattr(request, 'session', {})
    force_authenticate(request, user=company.admin)
    response = inline_image_attachment(request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = {
        'file': None,
        'company': company.id
    }
    request = factory.post(url, data)
    setattr(request, 'session', {})
    force_authenticate(request, user=company.admin)
    response = inline_image_attachment(request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
