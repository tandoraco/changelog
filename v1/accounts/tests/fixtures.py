import json
import random
import uuid

import pytest
from django.conf import settings
from faker import Faker

from frontend.forms.auth.utils import DEFAULT_PLAN_FEATURES
from v1.accounts.constants import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
from v1.accounts.models import User, ForgotPassword, CustomDomain, PricePlan, Subscription
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
def company(company_data):
    serializer = CompanySerializer(data=company_data)
    if serializer.is_valid():
        return serializer.save()

    return None


@pytest.fixture
def admin(company, company_data):
    return User.objects.get(email=company_data.get('email'))


@pytest.fixture
def user_data(company):
    return {
        'email': 'user@test.com',
        'password': 'User123.',
        'name': 'User',
        'company': company.id
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
def active_admin(admin):
    admin.is_active = True
    admin.save()
    admin.refresh_from_db()
    return admin


@pytest.fixture
def active_user(user):
    assert not user.is_active
    user.is_active = True
    user.save()
    user.refresh_from_db()
    return user


@pytest.fixture
def trial_user(admin):
    admin.company.is_trial_account = True
    admin.company.save()
    return admin


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
            'company_name': 'Test company',
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


@pytest.fixture
def custom_domain(company):
    tandora_url = settings.HOST + f'{company.company_name.lower()}/' + company.changelog_terminology.lower()
    return CustomDomain.objects.create(company=company,
                                       domain_name='https://test.tandora.co',
                                       tandora_url=tandora_url)


@pytest.fixture
def price_plan():
    data = {
        'name': 'Test plan',
        'monthly_price': 1.0,
        'yearly_price': 1.0 * 12,
        'plan_features': json.dumps(DEFAULT_PLAN_FEATURES)
    }
    return PricePlan.objects.create(**data)


@pytest.fixture
def subscription(price_plan, company):
    data = {
        'company': company,
        'plan': price_plan,
        'extra_plan_features': json.dumps({
            'users': 3
        })
    }

    return Subscription.objects.create(**data)


@pytest.fixture
def razorpay_webhook_data():
    return {'entity': 'event',
            'account_id': 'acc_DS11bHy6VsKIm1',
            'event': 'order.paid',
            'contains': ['payment', 'order'],
            'payload': {'payment': {'entity': {'id': 'pay_DbS5ICgza7ahUA',
                                               'entity': 'payment',
                                               'amount': 700000,
                                               'currency': 'INR',
                                               'status': 'captured',
                                               'order_id': 'order_DbS5EFZxo0DBCN',
                                               'invoice_id': None,
                                               'international': False,
                                               'method': 'upi',
                                               'amount_refunded': 0,
                                               'refund_status': None,
                                               'captured': True,
                                               'description': None,
                                               'card_id': None,
                                               'bank': None,
                                               'wallet': None,
                                               'vpa': 'test@test',
                                               'email': 'test@test.com',
                                               'contact': '123456789',
                                               'notes': {'email': 'test@test.com', 'phone': '123456789'},
                                               'fee': 16520,
                                               'tax': 2520,
                                               'error_code': None,
                                               'error_description': None,
                                               'created_at': 1572694014}},
                        'order': {'entity': {'id': 'order_DbS5EFZxo0DBCN',
                                             'entity': 'order',
                                             'amount': 700000,
                                             'amount_paid': 700000,
                                             'amount_due': 0,
                                             'currency': 'INR',
                                             'receipt': None,
                                             'offer_id': None,
                                             'status': 'paid',
                                             'attempts': 1,
                                             'notes': [],
                                             'created_at': 1572694011}}},
            'created_at': 1572694018}
