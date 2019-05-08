import copy

import pytest

from v1.core.models import Changelog
from v1.core.views import ChangelogViewset
from v1.utils.test_base.integration_test_base import ModelViewsetTestBase


@pytest.mark.integration
class TestChangelogViewset(ModelViewsetTestBase):
    viewset = ChangelogViewset
    url = "/api/v1/changelogs"
    model = Changelog

    def test_changelog_views(self, changelog1_data, changelog2_data, admin, published_changelog, unpublished_changelog):
        self.queryset = Changelog.objects.all()

        create_data = dict()
        create_data["valid_data"] = changelog1_data
        invalid_data = copy.deepcopy(changelog2_data)
        invalid_data["title"] = "a" * 201  # title can be at most 200 chars
        create_data["invalid_data"] = invalid_data

        update_data = dict()
        update_data["valid_data"] = {"content": "We are starting a changelog. Watch this space."}
        update_data["invalid_data"] = {"category": 100}  # category does not exists

        keys = ["title", "content", "category", "created_by", "last_edited_by"]
        self.run_all_assertions(admin, create_data, update_data, get_keys=keys)
