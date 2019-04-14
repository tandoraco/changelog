from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=7)
    deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'color')

    def __str__(self):
        return self.name
