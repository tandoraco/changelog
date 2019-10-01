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
        try:
            id = self.data['id']
            category = self.Meta.model.objects.get(id=id)
            cleaned_name = self.cleaned_data['name']

            if category.name == cleaned_name:
                return cleaned_name
        except KeyError:
            pass

        return validate_category_name(self.cleaned_data['name'], serializer=False)
