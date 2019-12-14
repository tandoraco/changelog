import json

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from v1.accounts.constants import CHANGELOG_TERMINOLOGY, MAX_EMAIL_LENGTH, USE_CASE_CHOICES
from v1.accounts.utils import UserManager
from v1.notifications.email import send_forgot_password_mail
from v1.utils import prettify_json


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

    @property
    def is_static_site(self):
        return self.use_case == 's'

    def settings_formatted(self):
        return prettify_json(self.settings)

    @property
    def theme(self):
        return self.settings.get('theme')

    def theme_meta(self, return_fields=True):
        from v1.core import models as core_models
        theme_name = self.settings.get('theme', 'default')
        theme_type = 'default'
        theme = 'public/static-site.html'
        fields = []

        try:
            static_site_theme = core_models.StaticSiteTheme.objects.filter(name__iexact=theme_name)[0]
            if static_site_theme.template_file:
                theme_type = 'file'
                theme = static_site_theme.template_file
            if static_site_theme.template_content:
                theme_type = 'content'
                theme = static_site_theme.template_content
            if return_fields:
                fields = static_site_theme.staticsitethemeconfig.fields.all()
        except (core_models.StaticSiteTheme.DoesNotExist, KeyError):
            pass

        return {
            'theme_type': theme_type,
            'theme': theme,
            'fields': fields
        }


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
        return prettify_json(self.data)


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


class CustomDomain(models.Model):
    company = models.OneToOneField(Company, on_delete=models.DO_NOTHING)
    domain_name = models.CharField(max_length=200, blank=False, null=False, unique=True, db_index=True)
    tandora_url = models.URLField(blank=False, null=False)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.domain_name} -> {self.tandora_url}'


post_save.connect(send_forgot_password_mail, sender=ForgotPassword)
