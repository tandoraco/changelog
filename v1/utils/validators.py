from rest_framework import serializers

from v1.categories.constants import INVALID_HEX_CODE


def validate_color(color):
    start = 1 if color.startswith("#") else 0

    if not color.startswith('#') and len(color) == 7:
        raise serializers.ValidationError(INVALID_HEX_CODE)

    try:
        int(f"{color[start:]}", 16)
    except ValueError:
        raise serializers.ValidationError(INVALID_HEX_CODE)

    return color
