from random import randint

from django.utils.text import slugify


def get_or_populate_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{slugify(instance.title[0:190])}-{randint(0, 5000)}'


def update_pinned_changelog(sender, instance, *args, **kwargs):
    if instance.deleted and instance.company.pinnedchangelog.changelog:
        pinned_changelog = instance.company.pinnedchangelog
        if pinned_changelog.changelog.id == instance.id:
            pinned_changelog.changelog = None
            pinned_changelog.save()


def remove_pinned_changelog(sender, instance, *args, **kwargs):
    if instance.company.pinnedchangelog.changelog:
        pinned_changelog = instance.company.pinnedchangelog
        if pinned_changelog.changelog.id == instance.id:
            pinned_changelog.changelog = None
            pinned_changelog.save()
