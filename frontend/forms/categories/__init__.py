from colorful.forms import RGBColorField
from django import forms

from v1.categories.models import Category
from v1.utils.validators import validate_color, validate_category_name


class CategoryForm(forms.ModelForm):
    color = RGBColorField()

    class Meta:
        model = Category
        fields = ['name', 'color']

    def clean_color(self):
        return validate_color(self.cleaned_data['color'], serializer=False)

    def clean_name(self):
        return validate_category_name(self.cleaned_data['name'], serializer=False)
