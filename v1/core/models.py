from django.db import models
from django.db.models.signals import pre_save, post_save
from tinymce.models import HTMLField

from v1.categories.models import Category
from v1.core import signals as core_signals


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


class InlineImageAttachment(models.Model):
    company = models.ForeignKey('Company', null=False, on_delete=models.CASCADE)
    file = models.ImageField(null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file.name


pre_save.connect(core_signals.get_or_populate_slug_field, sender=Changelog)
post_save.connect(core_signals.trigger_zapier_webhook, sender=Changelog)
