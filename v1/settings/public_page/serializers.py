from rest_framework import serializers

from v1.settings.public_page.models import PublicPage


class PublicPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicPage
        fields = '__all__'
