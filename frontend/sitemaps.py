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


class CustomSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 1

    def items(self):
        return (apps.get_model('v1', 'Company')).objects.filter(custom_sitemap=True).values_list('company_name')

    def location(self, obj):
        return reverse('company-specific-sitemap', kwargs={
            'company_name': slugify(obj[0])
        })


class ChangelogSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return apps.get_model('v1', 'Changelog').objects.filter(
            company__publicpage__hide_from_crawlers=False,
            published=True,
            deleted=False).order_by('company__company_name')

    def location(self, obj):
        return reverse('frontend-view-changelog-as-public', kwargs={
            'company': slugify(obj.company.company_name),
            'changelog_terminology': slugify(obj.company.changelog_terminology),
            'slug': obj.slug,
        })


SITEMAPS = {
    'companies': CompanySiteMap,
    'custom_sitemaps': CustomSiteMap,
    'changelogs': ChangelogSiteMap
}
