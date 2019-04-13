from v1.accounts.serializer import LoginSerializer, CompanySerializer, UserSerializer
from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase

from faker import Faker


class TestLoginSerializer(SerializerTestBase):
    serializer_class = LoginSerializer

    def test_login_serializer(self, company_data, user_data, create_admin, create_user):
        fake = Faker()
        fake_email = fake.email()
        invalid_password = "Hello123"
        data = []
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
