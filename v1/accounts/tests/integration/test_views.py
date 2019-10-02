import uuid

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.test import (APIRequestFactory, force_authenticate, APIClient)

from v1.accounts import views as account_views
from v1.accounts.constants import CHANGELOG_TERMINOLOGY as DEFAULT_CHANGELOG_TERMINOLOGY, \
    PASSWORD_LENGTH_VALIDATION_FAILED, RESET_TOKEN_INVALID
from v1.accounts.models import ForgotPassword

factory = APIRequestFactory()
client = APIClient()

@pytest.mark.django_db
@pytest.mark.integration
def test_create_company(company_data):
    # this password meets our constraints, so saving it for testing down the line
    original_password = company_data['password']
    original_email = company_data['email']
    url = reverse('v1-admin-and-company')

    # email not valid check for 422
    test_data = company_data
    test_data['email'] = "test"
    request = factory.post(url, test_data)
    response = account_views.create_company(request)
    assert response.status_code == 422

    # password constraints not met
    # check for 422 error
    company_data['password'] = 'hello'
    request = factory.post(url, company_data)
    response = account_views.create_company(request)
    assert response.status_code == 422

    company_data['email'] = original_email
    company_data['password'] = original_password
    request = factory.post(url, company_data)
    response = account_views.create_company(request)
    assert response.status_code == 201
    response_data = response.data
    assert response_data['admin'] == company_data['email']
    assert response_data[
               'changelog_terminology'] == DEFAULT_CHANGELOG_TERMINOLOGY  # default when no terminology provided

    changelog_terminology = "Blog"
    company_data['email'] = original_email + "com"
    company_data['website'] = "https://www.adhithyan.cm"
    company_data["changelog_terminology"] = changelog_terminology
    request = factory.post(url, company_data)
    response = account_views.create_company(request)
    assert response.status_code == 201
    assert response.data['changelog_terminology'] == changelog_terminology  # override default when provided


@pytest.mark.django_db
@pytest.mark.integration
def test_create_user(admin, user_data):
    url = reverse('v1-create-user')

    request = factory.post(url, user_data)
    response = account_views.create_user(request)
    assert response.status_code == 401  # no auth token was provided

    request = factory.post(url, user_data)
    force_authenticate(request, user=admin)
    response = account_views.create_user(request)
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.integration
def test_create_user_non_admin(user, user_data):
    fake_email = Faker().email()
    user_data['email'] = fake_email

    # the user is not a admin
    # so should raise 403 -> permission denied
    # only admins can create or add users to company
    url = reverse('v1-create-user')
    request = factory.post(url, user_data)
    force_authenticate(request, user=user)
    response = account_views.create_user(request)
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.integration
def test_forgot_password(user):
    url = reverse('v1-forgot-password')
    valid_data = {'email': user.email}
    invalid_data = {'email': Faker().email()}

    response = client.post(url, invalid_data, format='json')
    assert response.status_code == 422

    response = client.post(url, valid_data, format='json')
    assert response.status_code == 201
    assert 'token' in response.data


@pytest.mark.django_db
@pytest.mark.integration
def test_reset_password(forgot_password, valid_password, invalid_password):
    url = '/api/v1/reset-password/'
    valid_data = {'password': valid_password}
    invalid_data = {'password': invalid_password}

    response = client.post(url + forgot_password.token, data=invalid_data, format='json')
    assert response.status_code == 422
    assert str(response.data['password'][0]) == PASSWORD_LENGTH_VALIDATION_FAILED

    response = client.post(url + forgot_password.token, data=valid_data, format='json')
    assert response.status_code == 200

    response = client.post(url + forgot_password.token, data=valid_data, format='json')
    assert response.status_code == 422
    assert str(response.data['non_field_errors'][0]) == RESET_TOKEN_INVALID
