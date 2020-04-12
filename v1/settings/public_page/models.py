from colorful.fields import RGBColorField
from django.db import models

from frontend.custom.utils import SettingsMixin

DEFAULT_BLUE_COLOR = '#428bca'
WHITE_COLOR = '#FFFFFF'


class PublicPage(SettingsMixin, models.Model):
    company = models.OneToOneField('Company', null=False, on_delete=models.CASCADE)
    banner_color = RGBColorField(default=DEFAULT_BLUE_COLOR)
    banner_font_color = RGBColorField(default=WHITE_COLOR)
    font = models.TextField(blank=True, null=True)
    logo = models.ImageField(null=True, blank=True)
    _settings = models.TextField(blank=True, null=True, db_column='settings')
    hide_from_crawlers = models.BooleanField(default=True,
                                             help_text='Check this option, '
                                                       'if you don\'t want your page to be indexed by search engines.')

    def __str__(self):
        return f"{self.company}"
