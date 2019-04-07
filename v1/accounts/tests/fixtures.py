from v1.accounts.serializer import CompanySerializer, UserSerializer
from v1.accounts.models import User

import pytest


@pytest.fixture
def company_data():
    return {
        'email': 'test@test.com',
        'password': 'Test123.',
        'company_name': 'Test',
        'website': 'http://www.test.com',
        'name': 'Test Admin'
    }


@pytest.fixture
def create_admin(company_data):
    serializer = CompanySerializer(data=company_data)
    if serializer.is_valid():
        return serializer.save()

    return None


@pytest.fixture
def admin(create_admin, company_data):
    return User.objects.get(email=company_data.get('email'))


@pytest.fixture
def user_data():
    return {
        'email': 'user@test.com',
        'password': 'User123.',
        'name': 'User'
    }


@pytest.fixture
def create_user(user_data):
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        return serializer.save()

    return None


@pytest.fixture
def user(create_user, user_data):
    return User.objects.get(email=user_data.get('email'))
