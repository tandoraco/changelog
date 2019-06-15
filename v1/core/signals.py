from random import randint


def get_or_populate_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{instance.title.replace(" ", "-")}-{randint(0, 5000)}'
