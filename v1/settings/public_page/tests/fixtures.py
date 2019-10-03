import pytest

from v1.settings.public_page.serializers import PublicPageSerializer


@pytest.fixture
def public_page(company):
    data = {
        'company': company.id,
        'color': '#00ff00',
        'private_mode': True
    }

    serializer = PublicPageSerializer(data=data)
    serializer.is_valid()
    return serializer.save()
