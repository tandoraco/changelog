# Create your models here.
from django.db import models


class Instance(models.Model):
    admin_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    db_name = models.CharField(max_length=110, unique=True)
    db_user = models.CharField(max_length=100)
    db_password = models.CharField(max_length=50)
    db_host = models.CharField(max_length=20)
    db_port = models.CharField(max_length=4, default=5432)
    subdomain = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'<{self.admin_name}>'

    class Meta:
        db_table = 'master_instance_details'
