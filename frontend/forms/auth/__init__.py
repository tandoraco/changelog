from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _

from v1.accounts.constants import MAX_EMAIL_LENGTH, PASSWORD_INCORRECT_ERROR, EMAIL_NOT_FOUND_ERROR
from v1.accounts.models import User, Company
from v1.accounts.utils import verify_password


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


class CompanySignupForm():
    pass


class ForgotPasswordForm():
    pass


class ResetPasswordForm():
    pass


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
        fields = '__all__'


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
