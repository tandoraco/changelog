import random
import uuid

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from frontend.constants import PASSWORD_DOES_NOT_MATCH, USER_VERIFICATION_SUCCESS, USER_VERIFICATION_FAILED
from frontend.custom.test_utils import TandoraTestClient
from v1.accounts.constants import EMAIL_NOT_FOUND_ERROR, PASSWORD_INCORRECT_ERROR, PASSWORD_CONSTRAINS_NOT_MET, \
    INACTIVE_USER_ERROR
from v1.accounts.models import ForgotPassword, PendingUser


@pytest.mark.django_db
class TestAuthViews:
    client = TandoraTestClient()
    fake = Faker()

    def _test_inactive_user_login(self, data):
        url = reverse('frontend-login')

        response = self.client.post(url, data=data)
        # user will be inactive, as soon as the user is created. Should display inactive message.
        assert response.status_code == status.HTTP_200_OK
        assert response.context['form'].errors['email'][0] == INACTIVE_USER_ERROR

    @pytest.mark.django_db
    def test_login_logout(self, user, user_data):
        assert not user.is_active

        data = {
            'email': user.email,
            'password': user_data['password']
        }

        url = reverse('frontend-login')

        self._test_inactive_user_login(data)

        user.is_active = True
        user.save()

        response = self.client.post(url, data=data)
        # on successful login, redirect to staff changelogs page
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == '/staff'

        self.client.force_login(user)
        response = self.client.get('/staff')
        assert response.status_code == status.HTTP_200_OK

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

    @pytest.mark.django_db
    def test_forgot_reset_password(self, user, PASSWORD_CONSTRAINTS_NOT_MET=None):
        user.is_active = True
        user.save()

        forgot_password_url = reverse('frontend-forgot-password')

        # ensuring that no forgot password token exists, so we can
        # use .get() to get the token and perform a reset.
        assert ForgotPassword.objects.count() == 0

        response = self.client.get(forgot_password_url)
        response_content = response.content.decode()
        assert "Initiate password reset" in response_content
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

    @pytest.mark.django_db
    def test_user_account_verification(self, company, company_data):
        assert not company.admin.is_active

        assert PendingUser.objects.count() == 1
        pending_user = PendingUser.objects.get()

        data = {
            'email': company.admin.email,
            'password': company_data['password']
        }
        self._test_inactive_user_login(data)

        url = reverse('frontend-verify-user', args=(pending_user.uuid, ))
        response = self.client.get(url)
        assert 'login' in response['Location']
        self.client.assert_response_message(response, USER_VERIFICATION_SUCCESS)

        # After successful verification, the corresponding pending user will be deleted.
        assert PendingUser.objects.count() == 0
        with pytest.raises(PendingUser.DoesNotExist):
            PendingUser.objects.get(uuid=pending_user.uuid)

        # once an user is verified, the same verification link will become invalid
        response = self.client.get(url)
        self.client.assert_response_message(response, USER_VERIFICATION_FAILED)
