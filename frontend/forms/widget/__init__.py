from colorful.forms import RGBColorField
from django import forms

from v1.widget.models import Embed


class WidgetForm(forms.ModelForm):
    color = RGBColorField()
    javascript = forms.CharField(widget=forms.Textarea(attrs={"class": "mceNoEditor"}))
    css = forms.CharField(widget=forms.Textarea(attrs={"class": "mceNoEditor"}))

    class Meta:
        model = Embed
        fields = ['javascript', 'css', 'color', 'enabled']

    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)
