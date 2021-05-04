import uuid

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.management import call_command
from django.db import transaction
from django.utils.translation import ugettext as _

from frontend.constants import PASSWORD_DOES_NOT_MATCH, EMAIL_EXISTS_ERROR, WEBSITE_EXISTS_ERROR, INVALID_REFERRAL_CODE
from v1.accounts.constants import MAX_EMAIL_LENGTH, PASSWORD_INCORRECT_ERROR, EMAIL_NOT_FOUND_ERROR, \
    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, INACTIVE_USER_ERROR
from v1.accounts.models import User, Company, ForgotPassword, Affiliate, Referral
from v1.accounts.utils import verify_password, hash_password
from v1.accounts.validators import form_password_validator, form_no_symbols_validator, \
    form_black_listed_company_name_validator

REFERRAL_CODE = 'If you have a referral code provided by Tandora man (affiliate), provide here.'


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=MAX_EMAIL_LENGTH, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise forms.ValidationError(INACTIVE_USER_ERROR)
        except User.DoesNotExist:
            raise forms.ValidationError(_(EMAIL_NOT_FOUND_ERROR))

        return email

    def clean_password(self):
        password = self.cleaned_data.pop('password')
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not verify_password(user, password):
                raise forms.ValidationError(PASSWORD_INCORRECT_ERROR)
        except User.DoesNotExist:
            raise forms.ValidationError(EMAIL_NOT_FOUND_ERROR)

        return password


class BasicUserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=MIN_PASSWORD_LENGTH,
                               max_length=MAX_PASSWORD_LENGTH)

    def clean_email(self):
        email = self.data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(EMAIL_EXISTS_ERROR)
        except User.DoesNotExist:
            pass
        return email

    def clean_password(self):
        return form_password_validator(self.data.get('password'))


class StaffNewUserForm(BasicUserForm):
    company = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Company.objects.all())

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        data['password_hash'] = hash_password(data.pop('password'))
        return User.objects.create(**data)


class CompanySignupForm(BasicUserForm):
    website = forms.URLField(max_length=200, required=True)
    use_case = forms.CharField(widget=forms.HiddenInput, initial='c', required=False)
    company_name = forms.CharField(max_length=100)
    referral_code = forms.CharField(max_length=50, required=False, label=REFERRAL_CODE)
    # changelog_terminology = forms.CharField(max_length=50, initial='', required=False)

    def clean_website(self):
        website = self.data.get('website')
        try:
            Company.objects.get(website=website)
            raise forms.ValidationError(WEBSITE_EXISTS_ERROR)
        except Company.DoesNotExist:
            pass
        return website

    def clean_company_name(self):
        company_name = self.data.get('company_name')
        form_no_symbols_validator(company_name)
        form_black_listed_company_name_validator(company_name)
        return company_name

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')

        if referral_code:
            try:
                Referral.objects.get(referral_code=referral_code)
            except Referral.DoesNotExist:
                raise forms.ValidationError(INVALID_REFERRAL_CODE)

        return referral_code

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        call_command('create_company',
                     f'--email={data["email"]}',
                     f'--name={data["name"]}',
                     f'--password={data["password"]}',
                     f'--company_name={data["company_name"]}',
                     f'--website={data["website"]}',
                     f'--use_case={data["use_case"]}',
                     f'--changelog_terminology={data.get("changelog_terminology", "Changelog")}',
                     f'--referral_code={data.get("referral_code", None)}'
                     )


class ForgotPasswordForm(forms.ModelForm):
    token = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ForgotPassword
        fields = '__all__'

    def clean_token(self):
        return str(uuid.uuid4())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_(EMAIL_NOT_FOUND_ERROR))

        return email


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, validators=[form_password_validator])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(PASSWORD_DOES_NOT_MATCH)


class CompanyForm(forms.ModelForm):
    read_only_fields = [
        'admin',
        'website',
        'company_name',
    ]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        for field in self.read_only_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Company
        exclude = ['is_trial_account', 'created_time', 'use_case', '_settings']

    def clean_changelog_terminology(self):
        changelog_terminology = self.cleaned_data.get('changelog_terminology')
        return form_no_symbols_validator(changelog_terminology)


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ['email', 'name', ]


class TandoraAdminLoginForm(AuthenticationForm):

    def invalid_user(self, username=False, password=False):
        if username:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )

        if password:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'password': self.username_field.verbose_name}
            )

    def clean(self):
        userid = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if userid and password:
            self.user_cache = None
            try:
                user = User.objects.get(email=userid)
                if verify_password(user, password):
                    self.user_cache = user
            except User.DoesNotExist:
                pass

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class AffiliateSignupForm(forms.ModelForm):
    why = forms.CharField(widget=forms.TextInput, label='Why do you want to be the Tandora Man of Tandora?')

    class Meta:
        model = Affiliate
        fields = '__all__'
