from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=7)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'color')
