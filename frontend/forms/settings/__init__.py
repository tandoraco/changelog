from django import forms
from django.apps import apps

from frontend.forms.static_site import FONT_CHOICES


class PublicPageForm(forms.ModelForm):
    font = forms.ChoiceField(choices=FONT_CHOICES, required=True)

    class Meta:
        model = apps.get_model('v1', 'PublicPage')
        exclude = ('company', '_settings', 'logo')
