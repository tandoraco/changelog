from django import forms
from django.apps import apps

from frontend.constants import PUBLIC_PAGE_CHANGELOG_10_MULTIPLE_ERROR
from frontend.forms.static_site import FONT_CHOICES


class PublicPageForm(forms.ModelForm):
    font = forms.ChoiceField(choices=FONT_CHOICES, required=True)

    def clean_changelog_limit(self):
        changelog_limit = self.cleaned_data.get('changelog_limit')
        if changelog_limit % 10 != 0:
            raise forms.ValidationError(PUBLIC_PAGE_CHANGELOG_10_MULTIPLE_ERROR)
        return changelog_limit

    class Meta:
        model = apps.get_model('v1', 'PublicPage')
        exclude = ('company', '_settings', 'logo')
