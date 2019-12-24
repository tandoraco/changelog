import pytest
from django.urls import reverse
from rest_framework import status

from frontend.custom.test_utils import FrontEndFormViewTestBase, test_url

VIEW_CHANGELOGS = 'frontend-staff-index'
CREATE_CHANGELOG = 'frontend-create-changelog'
EDIT_CHANGELOG = 'frontend-edit-changelog'
DELETE_CHANGELOG = 'frontend-delete-changelog'


@pytest.mark.django_db
class TestFrontEndChangelogViews:

    def test_changelog_frontend_views(self, user, company, changelogs, changelog):
        urls = [
            test_url('create', reverse(CREATE_CHANGELOG)),
            test_url('edit', reverse(EDIT_CHANGELOG, kwargs={'id': changelog.id})),
            test_url('delete', reverse(DELETE_CHANGELOG, kwargs={'id': changelog.id})),
            test_url('view', reverse(VIEW_CHANGELOGS)),
        ]

        FrontEndFormViewTestBase(
            model_name='Tandora',
            urls=urls,
            fields=['title', 'content', 'category'],
            view_exclude_fields={'category'},
            user=user,
            company=company,
            queryset=changelogs,
            instance=changelog
        )

    def test_frontend_get_single_changelog(self, user, company, changelog):
        url = reverse('frontend-view-changelog', kwargs={'slug': changelog.slug})
        from frontend.custom.test_utils import TandoraTestClient
        client = TandoraTestClient()
        client.force_login(user)

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