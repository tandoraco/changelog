from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from tinymce.models import HTMLField

from v1.categories.models import Category
from v1.core import signals as core_signals
from v1.utils.validators import validate_image_size

AUTO_APPEND_CONTENT_HELP_TEXT = 'This content will be automatically added to the end of each changelog you create.' \
                                'This content will be visible only in public changelog details page.'


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
    featured_image = models.ImageField(null=True, blank=True, validators=[validate_image_size, ])

    def __str__(self):
        return f"{self.title}"

    @property
    def auto_append_content(self):
        try:
            return self.company.changelogsettings.auto_append_content
        except ChangelogSettings.DoesNotExist:
            return ''


class InlineImageAttachment(models.Model):
    company = models.ForeignKey('Company', null=False, on_delete=models.CASCADE)
    file = models.ImageField(null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class PinnedChangelog(models.Model):
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    changelog = models.OneToOneField('Changelog', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company} - {self.changelog}'


class ChangelogSettings(models.Model):
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    auto_append_content = HTMLField(blank=True, help_text=AUTO_APPEND_CONTENT_HELP_TEXT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company} - {self.auto_append_content}'

    class Meta:
        verbose_name_plural = 'Changelog Settings'


pre_save.connect(core_signals.get_or_populate_slug_field, sender=Changelog)
post_save.connect(core_signals.update_pinned_changelog, sender=Changelog)
post_delete.connect(core_signals.remove_pinned_changelog, sender=Changelog)
