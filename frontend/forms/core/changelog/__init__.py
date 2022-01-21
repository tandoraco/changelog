from django import forms

from v1.categories.models import Category
from v1.core.models import Changelog, PinnedChangelog, ChangelogSettings


class ChangelogForm(forms.ModelForm):
    published = forms.BooleanField(required=False, label='Publish Now\t', initial=True)

    class Meta:
        model = Changelog
        fields = ('title', 'content', 'category', 'featured_image', 'published',)

    def __init__(self, *args, **kwargs):
        super(ChangelogForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        request = initial['request']
        company_id = request.session['company-id']
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(company__id=company_id,
                                                                                          deleted=False))


class PinnedChangelogForm(forms.ModelForm):
    class Meta:
        model = PinnedChangelog
        fields = ('changelog',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        request = initial['request']
        company_id = request.session['company-id']
        self.fields['changelog'] = forms.ModelChoiceField(
            queryset=Changelog.objects.filter(company__id=company_id,
                                              published=True, deleted=False).order_by('-created_at'))


class ChangelogSettingsForm(forms.ModelForm):

    class Meta:
        model = ChangelogSettings
        fields = ('auto_append_content',)


class IncomingWebhookForm(forms.Form):
    title = forms.CharField(required=True, max_length=200)
    content = forms.CharField(widget=forms.TextInput)
