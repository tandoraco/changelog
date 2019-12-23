import pytest
from django.urls import reverse

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

