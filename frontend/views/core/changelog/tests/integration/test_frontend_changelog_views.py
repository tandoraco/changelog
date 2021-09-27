import mock
import pytest
from django.urls import reverse
from rest_framework import status

from frontend.constants import PLAN_LIMIT_REACHED_MESSAGE
from frontend.custom.test_utils import FrontEndFormViewTestBase, test_url
from frontend.forms.auth.utils import CHANGELOG_TESTING_LIMIT
from v1.core.models import Changelog

VIEW_CHANGELOGS = 'frontend-staff-index'
CREATE_CHANGELOG = 'frontend-create-changelog'
EDIT_CHANGELOG = 'frontend-edit-changelog'
DELETE_CHANGELOG = 'frontend-delete-changelog'


class TestFrontEndChangelogViews:

    @pytest.mark.django_db
    def test_changelog_frontend_views(self, active_user, company, changelogs, changelog):
        urls = [
            test_url('create', reverse(CREATE_CHANGELOG)),
            test_url('edit', reverse(EDIT_CHANGELOG, kwargs={'id': changelog.id})),
            test_url('delete', reverse(DELETE_CHANGELOG, kwargs={'id': changelog.id})),
            test_url('view', reverse(VIEW_CHANGELOGS)),
        ]

        FrontEndFormViewTestBase(
            model_name='Changelog',
            urls=urls,
            fields=['title', 'content', 'category'],
            view_exclude_fields={'category', 'content'},
            user=active_user,
            company=company,
            queryset=changelogs,
            instance=changelog
        )

    @pytest.mark.django_db
    def test_frontend_get_single_changelog(self, active_user, company, changelog):
        url = reverse('frontend-view-changelog', kwargs={'slug': changelog.slug})
        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(active_user)

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_content = response.content.decode()
        assert changelog.title in response_content
        assert changelog.content in response_content

        changelog.deleted = True
        changelog.save()
        changelog.refresh_from_db()
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_frontend_create__update_changelog(self, active_user, published_changelog_data, unpublished_changelog_data):
        url = reverse('frontend-create-changelog')

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(active_user)

        client.post(url, data=published_changelog_data)

        assert Changelog.objects.count() == 1

        client.post(url, data=unpublished_changelog_data)

        assert Changelog.objects.count() == 2

        changelog = Changelog.objects.first()
        url = reverse('frontend-edit-changelog', kwargs={'id': changelog.id})

        assert changelog.title != 'Test title 123'
        published_changelog_data['title'] = 'Test title 123'
        client.post(url, data=published_changelog_data)

        changelog.refresh_from_db()
        assert changelog.title == 'Test title 123'

        url = reverse('frontend-edit-changelog', kwargs={'id': 100})
        response = client.post(url, data=unpublished_changelog_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_frontend_changelog_limits(self, active_user, category):
        url = reverse('frontend-create-changelog')
        data = {
            'title': 'Test title',
            'content': 'Test category',
            'category': category.id
        }

        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(active_user)

        for i in range(CHANGELOG_TESTING_LIMIT):
            response = client.post(url, data=data)
            client.assert_response_message_icontains(response, 'success')

        response = client.post(url, data=data)
        client.assert_response_message(response, PLAN_LIMIT_REACHED_MESSAGE)