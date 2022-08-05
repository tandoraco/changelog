from django import forms

from v1.links.models import Link


class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ['title', 'url', ]
