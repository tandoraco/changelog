import pytest

from v1.widget.serializers import EmbedSerializer

COLOR = "#FF00FF"


@pytest.fixture
def embed_data(company):
    return {
        'company': company.id,
        'color': COLOR
    }


@pytest.fixture
def embed(embed_data):
    serializer = EmbedSerializer(data=embed_data)
    serializer.is_valid()
    return serializer.save()
