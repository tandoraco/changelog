import copy

import pytest

from v1.core.serializers import ChangelogSerializer
from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase


@pytest.mark.unit
class TestChangelogSerializer(SerializerTestBase):
    serializer_class = ChangelogSerializer

    def test_changelog_serializer_invalid_data(self, published_changelog_data, unpublished_changelog_data):
        data = []
        data.append(SerializerTestData(data=published_changelog_data,
                                       is_valid=False))  # without created and last edited by, so false
        data.append(SerializerTestData(data=unpublished_changelog_data, is_valid=False))
        data.append(data[0])  # duplicates allowed
        data.append(data[1])  # duplicates allowed
        self.run_data_assertions(test_data=data, create_db_entry=True)

        changelog_data = copy.deepcopy(published_changelog_data)
        del changelog_data["content"]
        del published_changelog_data["title"]
        del unpublished_changelog_data["category"]
        data = [
            SerializerTestData(data=changelog_data, is_valid=False),
            SerializerTestData(data=published_changelog_data, is_valid=False),
            SerializerTestData(data=unpublished_changelog_data, is_valid=False)
        ]
        self.run_data_assertions(test_data=data)

    def test_changelog_serializer_valid_data(self, published_changelog_data, unpublished_changelog_data, user, admin):
        data1 = copy.deepcopy(published_changelog_data)
        data1["created_by"] = admin.pk
        data1["last_edited_by"] = user.pk
        data2 = copy.deepcopy(unpublished_changelog_data)
        data2["created_by"] = user.pk
        data2["last_edited_by"] = user.pk
        data = [
            SerializerTestData(data=data1, is_valid=True),
            SerializerTestData(data=data2, is_valid=True)
        ]
        self.run_data_assertions(test_data=data)
