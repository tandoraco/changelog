from rest_framework import serializers

from v1.categories.constants import CATEGORY_EXISTS
from v1.categories.models import Category
from v1.utils.validators import validate_color


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('deleted',)
        read_only_fields = ('created_time',)

    def validate_color(self, color):
        return validate_color(color)

    def validate_name(self, name):
        try:
            Category.objects.get(name__iexact=name)
            raise serializers.ValidationError(CATEGORY_EXISTS)
        except Category.DoesNotExist:
            return name
