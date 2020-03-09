from django import forms

from v1.categories.models import Category
from v1.core.models import Changelog


class ChangelogForm(forms.ModelForm):
    published = forms.BooleanField(required=False, label='Publish Now\t')

    class Meta:
        model = Changelog
        fields = ('title', 'content', 'category')

    def __init__(self, *args, **kwargs):
        super(ChangelogForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        request = initial['request']
        company_id = request.session['company-id']
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(company__id=company_id,
                                                                                          deleted=False))

        if request.user.company.use_case == 's':
            self.fields['custom_url_path'] = forms.CharField(required=False, max_length=100)
            self.fields['custom_url_path'].label = 'Enter custom url path, ' \
                                                   'if you wish to access this page apart from usual url'
