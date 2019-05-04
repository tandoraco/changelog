from django.db import models


class PublicPage(models.Model):
    color = models.CharField(max_length=7)
    hide_from_crawlers = models.BooleanField(default=False)
    show_authors = models.BooleanField(default=False)
    private_mode = models.BooleanField(default=False)
