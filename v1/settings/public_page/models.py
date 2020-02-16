from colorful.fields import RGBColorField
from django.db import models

from frontend.custom.utils import SettingsMixin


class PublicPage(SettingsMixin, models.Model):
    company = models.ForeignKey('Company', null=False, on_delete=models.CASCADE)
    color = RGBColorField()
    hide_from_crawlers = models.BooleanField(default=True)
    _settings = models.TextField(blank=True, null=True, db_column='settings')

    def __str__(self):
        return f"{self.company}"
