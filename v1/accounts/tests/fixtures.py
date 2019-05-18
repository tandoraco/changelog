import random
import uuid

import pytest
from faker import Faker

from v1.accounts.constants import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
from v1.accounts.models import User, ForgotPassword
from v1.accounts.serializers import CompanySerializer, UserSerializer


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


@pytest.fixture
def valid_password():
    return "Fixture12@"


@pytest.fixture
def invalid_password():
    invalid_passwords = ["Hello12", "1" * (MIN_PASSWORD_LENGTH - 1), "2" * (MAX_PASSWORD_LENGTH + 1)]
    return random.choice(invalid_passwords)


@pytest.fixture
def valid_company_data(valid_password):
    fake = Faker()
    data = []
    for i in range(5):
        data.append({
            'email': fake.email(),
            'name': fake.name(),
            'password': valid_password,
            'company_name': fake.company(),
            'website': fake.url()
        })
    return data


@pytest.fixture
def invalid_company_data(invalid_password):
    fake = Faker()
    data = []
    for i in range(5):
        data.append({
            'email': fake.name(),
            'name': fake.name(),
            'password': invalid_password,
            'company_name': fake.company(),
            'website': fake.url()
        })
    return data


@pytest.fixture
def forgot_password(user, user_data):
    return ForgotPassword.objects.create(email=user_data['email'], token=str(uuid.uuid4()))
