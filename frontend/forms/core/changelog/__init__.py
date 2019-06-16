from django import forms

from v1.core.models import Changelog


class ChangelogForm(forms.ModelForm):
    published = forms.BooleanField(initial=True, label='Publish Now\t')

    class Meta:
        model = Changelog
        fields = ('title', 'content', 'category')
