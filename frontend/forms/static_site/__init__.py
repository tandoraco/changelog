from django import forms
from tinymce.widgets import TinyMCE

FONT_CHOICES = (
    ('https://fonts.googleapis.com/css?family=Poppins&display=swap', 'Poppins'),
    ('https://fonts.googleapis.com/css?family=Lato&display=swap', 'Lato'),
    ('https://fonts.googleapis.com/css?family=Open+Sans&display=swap', 'Open Sans'),
    ('https://fonts.googleapis.com/css?family=Gupter&display=swap', 'Gupter'),
)


class StaticSiteForm(forms.Form):
    company_name = forms.CharField(max_length=50)
    tag_line = forms.CharField(max_length=100)
    # company_logo_link = forms.URLField(required=False)
    font = forms.ChoiceField(choices=FONT_CHOICES, required=True)
    menu_1_title = forms.CharField(max_length=50, required=False)
    menu_1_link = forms.URLField(max_length=100, required=False)
    menu_2_title = forms.CharField(max_length=50, required=False)
    menu_2_link = forms.URLField(max_length=100, required=False)
    menu_3_title = forms.CharField(max_length=50, required=False)
    menu_3_link = forms.URLField(max_length=100, required=False)
    # menu_4_title = forms.CharField(max_length=50, required=False)
    # menu_4_link = forms.URLField(max_length=50, required=False)
    # menu_5_title = forms.CharField(max_length=50, required=False)
    # menu_5_link = forms.URLField(max_length=50, required=False)
    home_page_content = forms.CharField(widget=TinyMCE)
    image_slide_show_link_1 = forms.URLField(required=True)
    image_slide_show_link_2 = forms.URLField(required=True)
    facebook_profile = forms.URLField(required=False)
    twitter_profile = forms.URLField(required=False)
    privacy_policy_link = forms.URLField(required=True)
    terms_of_service_link = forms.URLField(required=True)
