import pytest

from v1.utils.test_base import SerializerTestData
from v1.utils.test_base.serializer_test_base import SerializerTestBase
from v1.widget.serializers import EmbedSerializer


@pytest.mark.unit
class TestWidgetSerializer(SerializerTestBase):
    serializer_class = EmbedSerializer

    def test_embed_serializer(self, company):
        data = [
            SerializerTestData(data={'company': company.id, 'color': 'asdfdfdf'}, is_valid=False),
            SerializerTestData(data={'company': company.id, 'color': '#000000'}, is_valid=True),
            SerializerTestData(data={'company': company.id, 'color': '000000'}, is_valid=True),
            SerializerTestData(data={'company': company.id,
                                     'color': '000000', 'javascript': '<script></script>', 'css': ''}, is_valid=True)
        ]

        self.run_data_assertions(data)
