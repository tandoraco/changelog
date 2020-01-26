from colorful.forms import RGBColorField
from django import forms

from frontend.constants import COMPANY_DOES_NOT_EXIST
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

            return validate_category_name(category.company, self.cleaned_data['name'], serializer=False)
        except KeyError:
            company = self.data['company']
            try:
                company = int(company)
                try:
                    from v1.accounts.models import Company
                    company = Company.objects.get(pk=company)
                    return validate_category_name(company, self.cleaned_data['name'], serializer=False)
                except Company.DoesNotExist:
                    raise
            except (ValueError, Company.DoesNotExist):
                raise forms.ValidationError(COMPANY_DOES_NOT_EXIST)
