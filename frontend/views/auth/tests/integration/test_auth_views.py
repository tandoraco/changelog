import random

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from frontend.custom.test_utils import TandoraTestClient
from v1.accounts.constants import EMAIL_NOT_FOUND_ERROR, PASSWORD_INCORRECT_ERROR


@pytest.mark.django_db
class TestAuthViews:
    client = TandoraTestClient()
    fake = Faker()

    def test_login_logout(self, user, user_data):
        data = {
            'email': user.email,
            'password': user_data['password']
        }

        url = reverse('frontend-login')
        response = self.client.post(url, data=data)
        # on successful login, redirect to staff changelogs page
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == '/staff/changelogs'

        # Incorrect email
        data['email'] = self.fake.email()
        response = self.client.post(url, data=data)
        response_content = response.content.decode()
        assert EMAIL_NOT_FOUND_ERROR in response_content

        # Incorrect password
        data['email'] = user.email
        data['password'] = user_data['password'] + str(random.randint(1, 100))
        response = self.client.post(url, data=data)
        response_content = response.content.decode()
        assert PASSWORD_INCORRECT_ERROR in response_content

        self.client.force_login(user)
        url = reverse('frontend-logout')
        response = self.client.get(url)
        # on successful logout, redirect to login page
        assert response.status_code == status.HTTP_200_OK
