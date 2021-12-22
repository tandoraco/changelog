from urllib.parse import unquote

from rest_framework import serializers


class PublicPageViewSerializer(serializers.Serializer):
    company_name = serializers.CharField(required=True, max_length=200)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate_company_name(self, company_name):
        company_name = unquote(company_name.replace('-', ' '))
        return company_name
