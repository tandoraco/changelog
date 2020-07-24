from django import forms
from django.db import transaction
from tinymce.widgets import TinyMCE

from v1.static_site.models import StaticSiteTheme

FONT_CHOICES = (
    ('https://fonts.googleapis.com/css?family=Poppins&display=swap', 'Poppins'),
    ('https://fonts.googleapis.com/css?family=Lato&display=swap', 'Lato'),
    ('https://fonts.googleapis.com/css?family=Open+Sans&display=swap', 'Open Sans'),
    ('https://fonts.googleapis.com/css?family=Nunito&display=swap', 'Nunito'),
    ('https://fonts.googleapis.com/css?family=Gupter&display=swap', 'Gupter'),
    ('https://fonts.googleapis.com/css?family=Roboto&display=swap', 'Roboto'),
    ('https://fonts.googleapis.com/css?family=Gelasio&display=swap', 'Gelasio'),
    ('https://fonts.googleapis.com/css?family=Montserrat&display=swap', 'Montserrat'),
    ('https://fonts.googleapis.com/css?family=Source+Sans+Pro&display=swap', 'Source Sans Pro'),
    ('https://fonts.googleapis.com/css?family=Lilita+One&display=swap', 'Lilita One'),
    ('https://fonts.googleapis.com/css?family=Oswald&display=swap', 'Oswald'),
    ('https://fonts.googleapis.com/css?family=Playfair+Display&display=swap', 'Playfair Display'),
    ('https://fonts.googleapis.com/css?family=Manrope&display=swap', 'Manrope'),
)
FONT_CHOICES = tuple(sorted(FONT_CHOICES, key=lambda f: f[1]))


class DefaultStaticSiteForm(forms.Form):
    company_name = forms.CharField(max_length=50)
    tag_line = forms.CharField(max_length=100)
    font = forms.ChoiceField(choices=FONT_CHOICES, required=True)
    menu_1_title = forms.CharField(max_length=50, required=False)
    menu_1_link = forms.URLField(max_length=100, required=False)
    menu_2_title = forms.CharField(max_length=50, required=False)
    menu_2_link = forms.URLField(max_length=100, required=False)
    menu_3_title = forms.CharField(max_length=50, required=False)
    menu_3_link = forms.URLField(max_length=100, required=False)
    home_page_content = forms.CharField(widget=TinyMCE)
    image_slide_show_link_1 = forms.URLField(required=True)
    image_slide_show_link_2 = forms.URLField(required=True)
    facebook_profile = forms.URLField(required=False)
    twitter_profile = forms.URLField(required=False)
    privacy_policy_link = forms.URLField(required=True)
    terms_of_service_link = forms.URLField(required=True)


class StaticSiteForm(forms.Form):

    def __init__(self, fields, *args, **kwargs):
        super(StaticSiteForm, self).__init__(*args, **kwargs)

        self.fields['font'] = forms.ChoiceField(choices=FONT_CHOICES, required=True)
        self.fields['home_page_content'] = forms.CharField(widget=TinyMCE)

        for field in fields:
            name, field = field.get_form_field_and_name()
            self.fields[name] = field


class ThemeForm(forms.Form):
    theme = forms.ModelChoiceField(queryset=StaticSiteTheme.objects.filter(is_private=False))

    def __init__(self, company, *args, **kwargs):
        super(ThemeForm, self).__init__(*args, **kwargs)
        self.company = company

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        theme_name = data['theme'].name
        settings = self.company.settings
        settings['theme'] = theme_name
        self.company.settings = settings
        self.company.save()
