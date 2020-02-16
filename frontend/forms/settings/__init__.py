from django import forms
from django.apps import apps


class PublicPageForm(forms.ModelForm):

    class Meta:
        model = apps.get_model('v1', 'PublicPage')
        fields = ('color', 'hide_from_crawlers', )
