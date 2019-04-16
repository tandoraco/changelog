from django.db import models

from v1.accounts.models import User
from v1.categories.models import Category


class Changelog(models.Model):
    title = models.CharField(blank=False, max_length=200)
    content = models.TextField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True)  # auto_now_add automatically adds time, only when a model is created
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_by")
    last_edited_at = models.DateTimeField(
        auto_now=True)  # auto_now automatically updates time, whenever a model is saved
    last_edited_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="last_edited_by")

    def __str__(self):
        return f"{self.title}\n{self.content}"
