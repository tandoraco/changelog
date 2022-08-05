from django.db import models


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
