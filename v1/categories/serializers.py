from rest_framework import serializers

from v1.categories.constants import CATEGORY_EXISTS, INVALID_HEX_CODE
from v1.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('deleted',)
        read_only_fields = ('created_time',)

    def validate_color(self, color):
        start = 1 if color.startswith("#") else 0

        if not color.startswith('#') and len(color) == 7:
            raise serializers.ValidationError(INVALID_HEX_CODE)

        try:
            int(f"{color[start:]}", 16)
        except ValueError:
            raise serializers.ValidationError(INVALID_HEX_CODE)

        return color

    def validate_name(self, name):
        try:
            Category.objects.get(name__iexact=name)
            raise serializers.ValidationError(CATEGORY_EXISTS)
        except Category.DoesNotExist:
            return name
