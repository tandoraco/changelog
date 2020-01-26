from rest_framework import serializers

from v1.categories.models import Category
from v1.utils.validators import validate_color, validate_category_name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('deleted', )
        read_only_fields = ('created_time',)

    def validate_color(self, color):
        return validate_color(color)

    def validate_name(self, name):
        company = self.initial_data.get('company')
        if isinstance(company, int):
            from v1.accounts.models import Company
            try:
                company = Company.objects.get(pk=company)
            except Company.DoesNotExist:
                company = None

        return validate_category_name(company, name)
