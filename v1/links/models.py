from django.db import models

DEVICE_TYPE_CHOICES = (
    ('mo', 'Mobile'),
    ('tb', 'Tablet'),
    ('pc', 'Laptop/Desktop/Personal Computer'),
    ('bo', 'Bot')
)


class Link(models.Model):
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=False, null=False)
    url = models.URLField(blank=False, null=False, db_index=True)
    temporary_redirect = models.BooleanField(default=False)
    thumbnail = models.ImageField(blank=True, null=True)
    important_link = models.BooleanField(default=False,
                                         verbose_name='Is this an Important Link ? If so, this will be ranked higher')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.url}'


class LinkLens(models.Model):
    link = models.ForeignKey('Link', on_delete=models.DO_NOTHING)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_type = models.CharField(max_length=2, choices=DEVICE_TYPE_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
