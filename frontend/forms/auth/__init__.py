from django import forms
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
