import pytest
from rest_framework import serializers

from v1.utils.test_base import SerializerTestData

SERIALIZER_CLASS_NONE = "Serializer class cannot be none."


@pytest.mark.django_db
class SerializerTestBase(object):
    serializer_class = None

    def run_data_assertions(self, test_data, create_db_entry=False):
        self.run_common_assertions()
        assert not self.serializer_class(data={}).is_valid()

        for data in test_data:
            # Check whether each entry conforms to our criteria
            assert isinstance(data, SerializerTestData)
            assert len(data) == 2
            assert isinstance(data.data, dict)
            assert isinstance(data.is_valid, bool)

            # Actual validations
            serializer = self.serializer_class(data=data.data)
            try:
                assert serializer.is_valid() == data.is_valid
            except AssertionError:
                print(serializer.errors)
                print(data.data)
                raise

            if serializer.is_valid() and data.is_valid and create_db_entry:
                serializer.save()

    def run_required_fields_assertions(self, data):
        pass

    def run_common_assertions(self):
        if not self.serializer_class:
            raise AttributeError(SERIALIZER_CLASS_NONE)

        assert isinstance(self.serializer_class, serializers.SerializerMetaclass)
