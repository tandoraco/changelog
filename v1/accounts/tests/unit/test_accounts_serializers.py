import uuid

import pytest
from faker import Faker

from v1.accounts.serializers import LoginSerializer, CompanySerializer, UserSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer
from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase


@pytest.mark.unit
class TestLoginSerializer(SerializerTestBase):
    serializer_class = LoginSerializer

    def test_login_serializer(self, company_data, user_data, company, create_user, invalid_password):
        fake = Faker()
        fake_email = fake.email()
        data = list()
        data.append(SerializerTestData(data={'email': company_data['email'], 'password': company_data['password']},
                                       is_valid=True))
        data.append(
            SerializerTestData(data={'email': user_data['email'], 'password': user_data['password']}, is_valid=True))
        data.append(SerializerTestData(data={'email': fake_email, 'password': "Hello123"},
                                       is_valid=False))  # email does not exist in db
        data.append(
            SerializerTestData(data={'email': user_data['email'], 'password': invalid_password}, is_valid=False))
        data.append(
            SerializerTestData(data={'email': company_data['email'], 'password': invalid_password}, is_valid=False))

        self.run_data_assertions(test_data=data)


@pytest.mark.unit
class TestUserSerializer(SerializerTestBase):
    serializer_class = UserSerializer

    def test_user_serializer(self, company_data, user_data, admin, valid_password, invalid_password):
        fake = Faker()
        data = list()
        data.append(
            SerializerTestData(data={'email': company_data['email'], 'name': 'Test', 'password': valid_password},
                               is_valid=False))  # already exisitng email so not valid
        data.append(SerializerTestData(data={'email': fake.email(), 'name': fake.name(), 'password': valid_password},
                                       is_valid=True))
        data.append(SerializerTestData(data={'email': fake.email()}, is_valid=False))  # password and name missing
        data.append(SerializerTestData(data={'name': fake.name()}, is_valid=False))  # email and password missing
        data.append(SerializerTestData(data={'email': fake.email(), 'name': fake.name()},
                                       is_valid=False))  # password is missing
        self.run_data_assertions(test_data=data)


@pytest.mark.unit
class TestCompanySerializer(SerializerTestBase):
    serializer_class = CompanySerializer

    def test_company_serializer(self, valid_company_data, invalid_company_data):
        data = list()
        data.extend([SerializerTestData(data=d, is_valid=True) for d in valid_company_data])
        data.extend([SerializerTestData(data=d, is_valid=False) for d in invalid_company_data])
        self.run_data_assertions(test_data=data)


@pytest.mark.unit
class TestForgotPasswordSerializer(SerializerTestBase):
    serializer_class = ForgotPasswordSerializer
    fake = Faker()

    def test_forgot_password_serializer(self, user):
        data = [
            SerializerTestData(data={'email': user.email, 'token': str(uuid.uuid4())}, is_valid=True),
            SerializerTestData(data={'email': user.email, 'token': "12345"}, is_valid=False),
            SerializerTestData(data={'email': self.fake.email(), 'token': str(uuid.uuid4())}, is_valid=False)
        ]
        self.run_data_assertions(data)


@pytest.mark.unit
class TestResetPasswordSerializer(SerializerTestBase):
    serializer_class = ResetPasswordSerializer

    def test_reset_password_serializer(self, forgot_password, valid_password, invalid_password):
        data = [
            SerializerTestData(data={'token': str(uuid.uuid4()), 'password': invalid_password}, is_valid=False),
            SerializerTestData(data={'token': str(uuid.uuid4()), 'password': valid_password}, is_valid=False),
            SerializerTestData(data={'token': forgot_password.token, 'password': invalid_password}, is_valid=False),
            SerializerTestData(data={'token': forgot_password.token, 'password': valid_password}, is_valid=True)
        ]
        self.run_data_assertions(data)
