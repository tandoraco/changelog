from django import forms
from rest_framework import serializers

from frontend.constants import COMPANY_DOES_NOT_EXIST
from v1.categories.constants import INVALID_HEX_CODE, CATEGORY_EXISTS, DELETED_CATEGORY
from v1.categories.models import Category


def validate_color(color, serializer=True):
    start = 1 if color.startswith("#") else 0

    obj = serializers if serializer else forms

    if not color.startswith('#') and len(color) == 7:
        raise obj.ValidationError(INVALID_HEX_CODE)

    try:
        int(f"{color[start:]}", 16)  # hexadecimal conversion
    except ValueError:
        raise obj.ValidationError(INVALID_HEX_CODE)

    return color


def validate_category_name(company, name, serializer=True):
    obj = serializers if serializer else forms
    if not company:
        raise obj.ValidationError(COMPANY_DOES_NOT_EXIST)
    try:
        category = Category.objects.get(company=company, name__iexact=name)
        if category.deleted:
            raise obj.ValidationError(DELETED_CATEGORY)
        else:
            raise obj.ValidationError(CATEGORY_EXISTS)
    except Category.DoesNotExist:
        return name
