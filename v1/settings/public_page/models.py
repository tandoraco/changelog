from colorful.fields import RGBColorField
from django.db import models

DEFAULT_BLUE_COLOR = '#428bca'
FONT_CHOICES = (
    ('https://fonts.googleapis.com/css?family=Poppins&display=swap', 'Poppins'),
    ('https://fonts.googleapis.com/css?family=Lato&display=swap', 'Lato'),
    ('https://fonts.googleapis.com/css?family=Open+Sans&display=swap', 'Open Sans'),
    ('https://fonts.googleapis.com/css?family=Gupter&display=swap', 'Gupter'),
    ('https://fonts.googleapis.com/css?family=Roboto&display=swap', 'Roboto'),
    ('https://fonts.googleapis.com/css?family=Gelasio&display=swap', 'Gelasio'),
    ('https://fonts.googleapis.com/css?family=Montserrat&display=swap', 'Montserrat'),
    ('https://fonts.googleapis.com/css?family=Source+Sans+Pro&display=swap', 'Source Sans Pro'),
    ('https://fonts.googleapis.com/css?family=Lilita+One&display=swap', 'Lilita One'),
    ('https://fonts.googleapis.com/css?family=Oswald&display=swap', 'Oswald'),
    ('https://fonts.googleapis.com/css?family=Playfair+Display&display=swap', 'Playfair Display')
)
FONT_CHOICES = tuple(sorted(FONT_CHOICES, key=lambda f: f[1]))


class PublicPage(models.Model):
    company = models.OneToOneField('Company', null=False, on_delete=models.CASCADE)
    color = RGBColorField(default=DEFAULT_BLUE_COLOR)
    hide_from_crawlers = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    tag_line = models.CharField(max_length=100, null=True, blank=True)
    font = models.CharField(max_length=100, choices=FONT_CHOICES,
                            default='https://fonts.googleapis.com/css?family=Lato&display=swap')
    company_logo = models.ImageField(null=True)

    def __str__(self):
        return f"{self.company}"
