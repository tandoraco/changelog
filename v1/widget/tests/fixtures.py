import pytest

from v1.widget.models import Embed

COLOR = "#FF00FF"


@pytest.fixture
def embed_data():
    return {
        'color': COLOR
    }


@pytest.fixture
def embed(embed_data):
    return Embed.objects.create(color=COLOR)
