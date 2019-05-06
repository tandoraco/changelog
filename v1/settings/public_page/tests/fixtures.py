import pytest

from v1.settings.public_page.models import PublicPage


@pytest.fixture
def public_page():
    data = {
        'color': '#00ff00',
        'private_mode': True
    }

    return PublicPage.objects.create(**data)
