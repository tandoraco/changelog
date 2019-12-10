import json

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from v1.accounts.constants import CHANGELOG_TERMINOLOGY, MAX_EMAIL_LENGTH, USE_CASE_CHOICES
from v1.accounts.utils import UserManager
from v1.notifications.email import send_forgot_password_mail


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
    is_trial_account = models.BooleanField(blank=False, default=True)
    use_case = models.CharField(max_length=1, choices=USE_CASE_CHOICES, default='c')
    created_time = models.DateTimeField(auto_now_add=True)
    _settings = models.TextField(blank=True, null=True, db_column='settings')

    def __str__(self):
        return f'{self.company_name}'

    def slug(self):
        return slugify(self.company_name)

    class Meta:
        verbose_name_plural = 'Companies'

    @property
    def settings(self):
        return json.loads(self._settings) if self._settings else {}

    @settings.setter
    def settings(self, value):
        self._settings = json.dumps(value)


class PricePlan(models.Model):
    name = models.CharField(max_length=100)
    monthly_price = models.FloatField()
    yearly_price = models.FloatField()
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    plan_features = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    company = models.OneToOneField(Company, null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(PricePlan, null=True, on_delete=models.DO_NOTHING)
    is_recurring = models.BooleanField(default=False)
    is_yearly = models.BooleanField(default=True)
    razorpay_account_id = models.CharField(max_length=50, unique=True, db_index=True)
    razorpay_data = models.TextField()
    last_paid_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{str(self.company)} is in {self.plan.name if self.plan else ""}'


class ForgotPassword(models.Model):
    token = models.UUIDField(db_index=True)
    email = models.EmailField()
    created_date = models.DateField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.email}, {self.token}"

    class Meta:
        unique_together = ('email', 'created_date')


class ClientToken(models.Model):
    token = models.UUIDField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token)


class AngelUser(models.Model):
    # this table is used to store data of user who has paid
    # but user details are not available
    # we will receive this data, via razorpay webhook
    email = models.EmailField(blank=False)
    data = models.TextField(blank=False)

    def __str__(self):
        return self.email

    def data_formatted(self):
        data = json.dumps(self.data, indent=2)

        formatter = HtmlFormatter(style='colorful')
        response = highlight(data, JsonLexer(), formatter)

        style = f'<style>{formatter.get_style_defs()}+</style></br>'

        return mark_safe(f'{style}{response}')


class Affiliate(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_no = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    why = models.TextField()

    def __str__(self):
        return f'{self.name} {self.email}'


class Referral(models.Model):
    referrer = models.OneToOneField(Affiliate, on_delete=models.DO_NOTHING, blank=False, null=False)
    referral_code = models.CharField(max_length=50, unique=True, db_index=True)
    conversion_count = models.PositiveIntegerField(default=0)
    company_ids = models.TextField(default='{}')

    def add_signup(self, value):
        ids = json.loads(self.company_ids)
        signed_up_ids = ids.get('signed_up_company_ids', [])
        signed_up_ids.append(value)
        ids['signed_up_company_ids'] = signed_up_ids
        self.company_ids = json.dumps(ids)
        self.conversion_count += 1
        self.save()

    def __str__(self):
        return self.referrer.name


post_save.connect(send_forgot_password_mail, sender=ForgotPassword)
