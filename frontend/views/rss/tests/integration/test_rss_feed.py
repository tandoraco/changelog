import pytest
from django.urls import reverse
from django.test import Client

from v1.utils import html_2_text


@pytest.mark.django_db
def test_rss_feed(changelogs):
    company = changelogs[0].company
    path = reverse('public-rss-feed',
                   kwargs={'company': company.company_name, 'changelog_terminology': company.changelog_terminology})
    client = Client()
    response = client.get(path)
    assert response.status_code == 200
    rss = response.content.decode()

    for changelog in changelogs:
        if changelog.published and not changelog.deleted:
            assert changelog.title in rss
            assert html_2_text(changelog.content) in rss
        else:
            assert changelog.title not in rss

    # Company does not exist, raise 404
    path = reverse('public-rss-feed',
                   kwargs={'company': 'dsfdf', 'changelog_terminology': 'ddff'})
    response = client.get(path)
    assert response.status_code == 404
