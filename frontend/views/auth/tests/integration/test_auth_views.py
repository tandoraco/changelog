import random
import uuid

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from frontend.constants import PASSWORD_DOES_NOT_MATCH
from frontend.custom.test_utils import TandoraTestClient
from v1.accounts.constants import EMAIL_NOT_FOUND_ERROR, PASSWORD_INCORRECT_ERROR, PASSWORD_CONSTRAINS_NOT_MET
from v1.accounts.models import ForgotPassword


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
        assert response.url == '/staff'

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

        response = self.client.get(url)
        response_content = response.content.decode().lower()
        assert "login" in response_content
        assert "email" in response_content
        assert "password" in response_content

        self.client.force_login(user)
        url = reverse('frontend-logout')
        response = self.client.get(url)
        # on successful logout, redirect to login page
        assert response.status_code == status.HTTP_200_OK

    def test_forgot_reset_password(self, user, PASSWORD_CONSTRAINTS_NOT_MET=None):
        forgot_password_url = reverse('frontend-forgot-password')

        # ensuring that no forgot password token exists, so we can
        # use .get() to get the token and perform a reset.
        assert ForgotPassword.objects.count() == 0

        response = self.client.get(forgot_password_url)
        response_content = response.content.decode()
        assert "Forgot Password" in response_content
        assert 'Email' in response_content

        # Invalid email
        data = {
            'email': self.fake.email()
        }
        response = self.client.post(forgot_password_url, data=data)
        response_content = response.content.decode()
        assert EMAIL_NOT_FOUND_ERROR in response_content

        data['email'] = user.email
        response = self.client.post(forgot_password_url, data=data)
        response_content = response.content.decode()
        # on success will be redirected to login page
        assert response.status_code == status.HTTP_302_FOUND

        assert ForgotPassword.objects.count() == 1
        forgot_password = ForgotPassword.objects.get()
        assert forgot_password.token
        assert forgot_password.email == user.email

        # token not in reset password url should throw error and redirect to login page
        reset_password_url = reverse('frontend-reset-password', kwargs={'token': str(uuid.uuid4())})
        response = self.client.get(reset_password_url)
        assert response.status_code == status.HTTP_302_FOUND

        reset_password_url = reverse('frontend-reset-password', kwargs={'token': forgot_password.token})
        response = self.client.get(reset_password_url)
        assert response.status_code == status.HTTP_200_OK

        data = {
            'password': 'DSFSDFDF',
            'confirm_password': 'DSFSDFDF'
        }
        response = self.client.post(reset_password_url, data=data)
        response_content = response.content.decode()
        assert PASSWORD_CONSTRAINS_NOT_MET in response_content

        new_password = 'Pytest123.'
        data = {
            'password': new_password,
            'confirm_password': 'Abcdefg'
        }
        response = self.client.post(reset_password_url, data=data)
        response_content = response.content.decode()
        assert PASSWORD_DOES_NOT_MATCH in response_content

        data['confirm_password'] = data['password']
        response = self.client.post(reset_password_url, data=data)
        # on successful reset, we will be redirected to login page
        assert response.status_code == status.HTTP_302_FOUND

        # after successful reset forgot password token will be deleted.
        assert ForgotPassword.objects.count() == 0

        # login with new password
        url = reverse('frontend-login')
        data = {
            'email': user.email,
            'password': new_password
        }
        response = self.client.post(url, data=data)
        # on successful login, redirect to staff changelogs page
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == '/staff'
