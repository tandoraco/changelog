import pytest
from django.urls import reverse
from faker import Faker
from knox import views as auth_views
from rest_framework.test import (APIRequestFactory, RequestsClient,
                                 force_authenticate)

from v1.accounts import views as account_views

factory = APIRequestFactory()


@pytest.mark.django_db
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

@pytest.mark.django_db
def test_create_user(admin, user_data, company_data):
    url = reverse('v1-create-user')

    request = factory.post(url, user_data)
    response = account_views.create_user(request)
    assert response.status_code == 401  # no auth token was provided

    request = factory.post(url, user_data)
    force_authenticate(request, user=admin)
    response = account_views.create_user(request)
    assert response.status_code == 201


@pytest.mark.django_db
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
