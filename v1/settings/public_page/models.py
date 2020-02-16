from colorful.fields import RGBColorField
from django.db import models

from frontend.custom.utils import SettingsMixin


DEFAULT_BLUE_COLOR = '#428bca'


class PublicPage(SettingsMixin, models.Model):
    company = models.OneToOneField('Company', null=False, on_delete=models.CASCADE)
    color = RGBColorField(default=DEFAULT_BLUE_COLOR)
    hide_from_crawlers = models.BooleanField(default=True)
    _settings = models.TextField(blank=True, null=True, db_column='settings')

    def __str__(self):
        return f"{self.company}"
