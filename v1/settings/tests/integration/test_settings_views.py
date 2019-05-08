import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from v1.accounts.models import Company
from v1.settings import views as settings_views


def _get_settings_request():
    factory = APIRequestFactory()
    url = reverse('v1-settings')
    return factory.get(url)


@pytest.mark.integration
@pytest.mark.django_db
def test_settings_views_without_data(user):
    request = _get_settings_request()
    response = settings_views.settings(request)
    assert response.status_code == 401

    force_authenticate(request, user=user)
    # company is not yet created, so error is thrown
    with pytest.raises(Company.DoesNotExist):
        response = settings_views.settings(request)


@pytest.mark.integration
@pytest.mark.django_db
def test_settings_view_with_data_as_user(user, admin, public_page, category):
    request = _get_settings_request()
    force_authenticate(request, user=user)
    response = settings_views.settings(request)
    response_data = response.data
    assert response.status_code == 200
    assert isinstance(response_data, dict)

    expected_keys = ["company", "user_profile", "public_page", "categories"]
    assert all(key in expected_keys for key in response_data.keys())

    for key in ["company", "user_profile", "public_page"]:
        assert isinstance(response_data[key], dict)
    assert isinstance(response_data["categories"], list)
