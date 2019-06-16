from random import randint


def get_or_populate_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{instance.title[0:190].replace(" ", "-")}-{randint(0, 5000)}'
