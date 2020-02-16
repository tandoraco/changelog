from django.apps import apps
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.text import slugify


class CompanySiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return (apps.get_model('v1', 'Company').objects.filter(publicpage__hide_from_crawlers=False).values_list(
            'company_name'))

    def location(self, obj):
        return reverse('frontend-company-public-index', kwargs={
            'company': slugify(obj[0])
        })


SITEMAPS = {
    'companies': CompanySiteMap
}
