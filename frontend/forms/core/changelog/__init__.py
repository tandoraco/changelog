from django import forms

from v1.core.models import Changelog


class NewChangelogForm(forms.ModelForm):
    published = forms.BooleanField(required=True, initial=False, label='Publish Now\t')

    class Meta:
        model = Changelog
        fields = ('title', 'content', 'category', 'published')
