from urllib.parse import urljoin

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import Http404
from django.urls import reverse
from django.utils.text import slugify

from frontend.custom.utils import get_changelogs_from_company_name_and_changelog_terminology
from v1.utils import html_2_text


class PublicChangelogFeed(Feed):
    title = ""
    link = ""
    description = ""
    company = None
    changelog_terminology = None
    company_name = None

    def __call__(self, request, *args, **kwargs):
        self.company = str(kwargs['company'])
        self.company_name = self.company.lower().replace('-', '')
        self.changelog_terminology = kwargs['changelog_terminology']
        self.title = f'{self.company_name.title()} RSS Feed'
        self.description = f'Recent 20 {self.changelog_terminology} from {self.company_name.title()}'
        return super().__call__(request, *args, **kwargs)

    def items(self):
        changelogs = get_changelogs_from_company_name_and_changelog_terminology(self.company,
                                                                                self.changelog_terminology)[:20]
        if not changelogs:
            raise Http404
        return changelogs

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return html_2_text(item.content)

    def item_link(self, item):
        return urljoin(settings.HOST, reverse('frontend-view-changelog-as-public',
                                              kwargs={'company': slugify(item.company.company_name),
                                                      'changelog_terminology': slugify(
                                                          item.company.changelog_terminology),
                                                      'slug': str(item.slug)}))
