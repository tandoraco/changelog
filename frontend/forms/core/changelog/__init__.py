from django import forms

from v1.categories.models import Category
from v1.core.models import Changelog


class ChangelogForm(forms.ModelForm):
    published = forms.BooleanField(required=False, label='Publish Now\t', initial=True)

    class Meta:
        model = Changelog
        fields = ('title', 'content', 'category', 'featured_image', 'published', )

    def __init__(self, *args, **kwargs):
        super(ChangelogForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        request = initial['request']
        company_id = request.session['company-id']
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(company__id=company_id,
                                                                                          deleted=False))
