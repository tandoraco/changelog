from django.urls import reverse
from rest_framework import status

from frontend.constants import PLAN_LIMIT_REACHED_MESSAGE
from frontend.custom.test_utils import FrontEndTestBase
from v1.accounts import models as accounts_models


class TestManageUsers(FrontEndTestBase):

    def test_user_list(self, active_admin, active_user):
        url = reverse('frontend-view-users')

        self.run_admin_endpoint_test(url, active_admin, active_user)

        self.client.force_login(active_admin)
        response = self.client.get(url)

        response_content = response.content.decode()
        assert active_user.email in response_content

        assert response.context['object_list']
        response_queryset = response.context['object_list']
        assert len(response_queryset) == 1
        # the admin who is performing the action won't be included in queryset
        # only  other users will be included
        for obj in response_queryset:
            assert str(obj) != str(active_admin)

        response_content = response_content.lower()
        assert 'create user' in response_content
        # the user in the above response is an active user, so deactivate should be found in response
        assert 'deactivate' in response_content
        assert 'reset password' in response_content

        # make the active user inactive and make the request. Now activate should be found in response
        active_user.is_active = False
        active_user.save()
        active_user.refresh_from_db()

        response = self.client.get(url)
        response_content = response.content.decode().lower()
        assert 'activate' in response_content and 'deactivate' not in response_content

    def test_create_user(self, active_admin, active_user, subscription):
        url = reverse('frontend-create-user')

        # Fixtures create an active admin and active user, so 2 users
        assert accounts_models.User.objects.count() == 2
        self.run_admin_endpoint_test(url, active_admin, active_user)

        # Subscription allows 3 users for our test company as per fixture
        # so one more user can be created. after this it should not allow user creation
        data = {
            'email': self.faker.email(),
            'name': self.faker.name(),
            'password': 'User123.@',
            'company': active_admin.company.id
        }
        self.client.force_login(active_admin)
        response = self.client.post(url, data)
        self.client.assert_response_message_icontains(response, 'successfully create user')

        assert accounts_models.User.objects.count() == 3

        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        assert 'staff/manage/users' in response['Location']

    def test_edit_user(self, active_admin, active_user):
        url = reverse('frontend-edit-user', args=(active_user.id, ))

        self.run_admin_endpoint_test(url, active_admin, active_user)

        new_name = self.faker.name()
        assert active_user.name != new_name

        data = {
            'email': active_user.email,
            'name': new_name
        }
        self.client.force_login(active_admin)
        self.client.post(url, data)

        active_user.refresh_from_db()
        assert active_user.name == new_name

    def test_activate_user(self, active_admin, user):
        assert not user.is_active
        url = reverse('frontend-activate-user', args=(user.id,))

        self.client.force_login(active_admin)
        self.client.get(url)

        user.refresh_from_db()
        assert user.is_active

    def test_deactivate_user(self, active_admin, active_user):
        assert active_user.is_active
        url = reverse('frontend-deactivate-user', args=(active_user.id,))

        self.client.force_login(active_admin)
        self.client.get(url)

        active_user.refresh_from_db()
        assert not active_user.is_active

    def test_admin_reset_password(self, active_admin, active_user):
        url = reverse('frontend-admin-reset-password', args=(active_user.id,))

        from v1.accounts.models import ForgotPassword
        assert ForgotPassword.objects.count() == 0

        # an admin can reset password for an active user only. (current behaviour)
        self.login = self.client.force_login(active_admin)
        self.client.get(url)

        assert ForgotPassword.objects.count() == 1

        active_user.is_active = False
        active_user.save()
        active_user.refresh_from_db()

        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND