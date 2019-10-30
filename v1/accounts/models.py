from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.text import slugify

from v1.accounts.constants import CHANGELOG_TERMINOLOGY, MAX_EMAIL_LENGTH
from v1.accounts.utils import UserManager


class User(AbstractBaseUser):
    company = models.ForeignKey('Company', null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, db_index=True, unique=True)
    password_hash = models.CharField(
        max_length=100)
    is_locked = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return "[{} : {}]".format(
            self.email, self.name)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_active and self.is_superuser


class Company(models.Model):
    admin = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='company_admin')
    website = models.URLField(max_length=200, blank=False, unique=True)
    company_name = models.CharField(max_length=100)
    changelog_terminology = models.CharField(max_length=50, default=CHANGELOG_TERMINOLOGY)
    is_trial_account = models.BooleanField(blank=False, default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.company_name}'

    def slug(self):
        return slugify(self.company_name)


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
