import re

from django import forms
from django.db import models
from django.db.models.signals import pre_save
from tinymce.widgets import TinyMCE

from v1.static_site.signals import snake_case_field_name

STATIC_SITE_FIELD_CHOICES = (
    ('c', 'char'),
    ('t', 'text'),
    ('u', 'link'),
    ('e', 'email'),
    ('p', 'phone'),
)
PHONE_NUMBER_REGEXP = re.compile(r"^[\+]?\d{6,29}$")


class StaticSiteTheme(models.Model):
    name = models.CharField(max_length=50)
    template_file = models.CharField(max_length=100, blank=True, null=True)
    template_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class StaticSiteField(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    type = models.CharField(max_length=2, choices=STATIC_SITE_FIELD_CHOICES)
    required = models.BooleanField(default=False)
    max_length = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.get_type_display()} - [required: {self.required}]'

    def get_form_field_and_name(self):
        field_type = self.get_type_display()

        if field_type == 'char':
            return self.name, forms.CharField(max_length=self.max_length or 50, required=self.required)
        elif field_type == 'text':
            return self.name, forms.CharField(widget=TinyMCE, required=self.required)
        elif field_type == 'link':
            return self.name, forms.URLField(max_length=self.max_length or 100, required=self.required)
        elif field_type == 'email':
            return self.name, forms.EmailField(required=self.required)
        else:
            return self.name, forms.RegexField(regex=PHONE_NUMBER_REGEXP, required=self.required)


class StaticSiteThemeConfig(models.Model):
    theme = models.OneToOneField(StaticSiteTheme, on_delete=models.CASCADE)
    fields = models.ManyToManyField(StaticSiteField)

    def __str__(self):
        return f'{self.theme.name} config'


pre_save.connect(snake_case_field_name, sender=StaticSiteField)
