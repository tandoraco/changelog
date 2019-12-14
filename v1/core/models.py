from django import forms
from django.db import models
from django.db.models.signals import pre_save
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

from v1.categories.models import Category
from v1.core.signals import get_or_populate_slug_field, snake_case_field_name

STATIC_SITE_FIELD_CHOICES = (
    ('c', 'char'),
    ('t', 'text'),
    ('u', 'link')
)


class Changelog(models.Model):
    from v1.accounts.models import User, Company

    company = models.ForeignKey(Company, null=False, on_delete=models.DO_NOTHING)
    title = models.CharField(blank=False, max_length=200, db_index=True)
    slug = models.SlugField(blank=True, max_length=200, db_index=True)
    content = HTMLField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True)  # auto_now_add automatically adds time, only when a model is created
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_by")
    last_edited_at = models.DateTimeField(
        auto_now=True)  # auto_now automatically updates time, whenever a model is saved
    last_edited_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="last_edited_by")
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}\n{self.id}"


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
        else:
            return self.name, forms.URLField(max_length=self.max_length or 100, required=self.required)


class StaticSiteThemeConfig(models.Model):
    theme = models.OneToOneField(StaticSiteTheme, on_delete=models.CASCADE)
    fields = models.ManyToManyField(StaticSiteField)

    def __str__(self):
        return f'{self.theme.name} config'


pre_save.connect(get_or_populate_slug_field, sender=Changelog)
pre_save.connect(snake_case_field_name, sender=StaticSiteField)
