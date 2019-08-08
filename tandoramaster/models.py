# Create your models here.
from django.db import models

from v1.accounts.constants import MAX_EMAIL_LENGTH


class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=MAX_EMAIL_LENGTH)
    db_name = models.CharField(max_length=110)
    subdomain = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'<{self.name}>'
