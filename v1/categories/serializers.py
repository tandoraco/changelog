import string

from rest_framework import serializers

from v1.categories.constants import CATEGORY_EXISTS, INVALID_HEX_CODE
from v1.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('deleted', )
        read_only_fields = ('created_time', )

    def validate_color(self, color):
        start = 0
        if color.startswith("#"):
            start = 1
        valid_hex = all(c in string.hexdigits for c in color[start:])

        if not valid_hex:
            raise serializers.ValidationError(INVALID_HEX_CODE)

        return color

    def validate_name(self, name):
        try:
            Category.objects.get(name__iexact=name)
            raise serializers.ValidationError(CATEGORY_EXISTS)
        except Category.DoesNotExist:
            return name
