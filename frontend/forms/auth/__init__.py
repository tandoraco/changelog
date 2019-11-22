import uuid

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.management import call_command
from django.db import transaction
from django.utils.translation import ugettext as _

from frontend.constants import PASSWORD_DOES_NOT_MATCH, EMAIL_EXISTS_ERROR, WEBSITE_EXISTS_ERROR
from v1.accounts.constants import MAX_EMAIL_LENGTH, PASSWORD_INCORRECT_ERROR, EMAIL_NOT_FOUND_ERROR, \
    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
from v1.accounts.models import User, Company, ForgotPassword, Affiliate
from v1.accounts.utils import verify_password
from v1.accounts.validators import form_password_validator


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=MAX_EMAIL_LENGTH, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
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


class CompanySignupForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your name')
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=MIN_PASSWORD_LENGTH,
                               max_length=MAX_PASSWORD_LENGTH)
    website = forms.URLField(max_length=200, required=True)
    company_name = forms.CharField(max_length=100)
    # changelog_terminology = forms.CharField(max_length=50, initial='', required=False)

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

    def clean_website(self):
        website = self.data.get('website')
        try:
            Company.objects.get(website=website)
            raise forms.ValidationError(WEBSITE_EXISTS_ERROR)
        except Company.DoesNotExist:
            pass
        return website

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        call_command('create_company',
                     f'--email={data["email"]}',
                     f'--name={data["name"]}',
                     f'--password={data["password"]}',
                     f'--company_name={data["company_name"]}',
                     f'--website={data["website"]}',
                     f'--changelog_terminology={data.get("changelog_terminology", "Changelog")}'
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
        exclude = ['is_trial_account', 'created_time']


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
