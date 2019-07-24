from django import forms
from django.forms import TextInput

from v1.categories.models import Category
from v1.utils.validators import validate_color, validate_category_name


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }

    def clean_color(self):
        return validate_color(self.cleaned_data['color'], serializer=False)

    def clean_name(self):
        return validate_category_name(self.cleaned_data['name'], serializer=False)
