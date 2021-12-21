from colorful.fields import RGBColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext as _

from frontend.custom.utils import SettingsMixin
from v1.utils.validators import validate_logo

DEFAULT_BLUE_COLOR = '#428bca'
WHITE_COLOR = '#FFFFFF'
DEFAULT_PUBLIC_PAGE_CHANGELOG_LIMIT = 10
MAX_PUBLIC_PAGE_CHANGELOG_LIMIT = 50


class PublicPage(SettingsMixin, models.Model):
    company = models.OneToOneField('Company', null=False, on_delete=models.CASCADE)
    banner_color = RGBColorField(default=DEFAULT_BLUE_COLOR)
    banner_font_color = RGBColorField(default=WHITE_COLOR)
    banner_title = models.CharField(blank=True, null=True, max_length=50,
                                    help_text=_('(Optional) If not provided, company name will be used.'))
    banner_tag_line = models.CharField(blank=True, null=True, max_length=200,
                                       help_text=_('(Optional) If not provided, changelog terminology will be used.'))
    seo_title = models.CharField(blank=True, null=True, max_length=200,
                                 help_text=_('(Optional) This will used to inform search engines about the '
                                             'content and keywords of your public page.'))
    font = models.TextField(blank=True, null=True)
    logo = models.ImageField(null=True, blank=True, validators=[validate_logo, ],
                             help_text=_('Max file size: 500 kb'))
    changelog_limit = models.PositiveIntegerField(
        default=DEFAULT_PUBLIC_PAGE_CHANGELOG_LIMIT,
        validators=[
            MinValueValidator(DEFAULT_PUBLIC_PAGE_CHANGELOG_LIMIT),
            MaxValueValidator(MAX_PUBLIC_PAGE_CHANGELOG_LIMIT)],
        help_text=_('Maximum number of changelogs to show in public page. (Minimum  10 Maximum 50)'))
    hide_from_crawlers = models.BooleanField(
        default=True,
        help_text=_('Check this option, if you don\'t want your page to be indexed by search engines.'))

    def __str__(self):
        return f"{self.company}"

    class Meta:
        verbose_name = _('Public Page Settings')
        verbose_name_plural = _('Public Page Settings')
