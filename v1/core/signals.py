from random import randint

from django.utils.text import slugify


def get_or_populate_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{slugify(instance.title[0:190])}-{randint(0, 5000)}'
