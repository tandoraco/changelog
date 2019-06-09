from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from v1.accounts.constants import CHANGELOG_TERMINOLOGY, MAX_EMAIL_LENGTH


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, db_index=True, unique=True)
    password_hash = models.CharField(
        max_length=100)
    is_locked = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return "[{} : {}]".format(
            self.email, self.name)


class Company(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(max_length=200, blank=False, unique=True)
    company_name = models.CharField(max_length=100)
    changelog_terminology = models.CharField(max_length=50, default=CHANGELOG_TERMINOLOGY)
    created_time = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return str(self.admin)


class ForgotPassword(models.Model):
    token = models.UUIDField(db_index=True)
    email = models.EmailField(MAX_EMAIL_LENGTH, unique=True)

    def __str__(self):
        return f"{self.email}, {self.token}"


class ClientToken(models.Model):
    token = models.UUIDField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token)
