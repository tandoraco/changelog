from rest_framework import serializers

from v1.settings.public_page.models import PublicPage
from v1.utils import validators


class PublicPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicPage
        fields = '__all__'

    def validate_color(self, color):
        return validators.validate_color(color)

    def to_representation(self, instance):
        return {
            "company": instance.company.id,
            "color": instance.color,
            "hide_from_crawlers": instance.hide_from_crawlers,
            "settings": instance.settings
        }
