from django.db import transaction
from rest_framework import serializers

from v1.static_site.models import StaticSiteField


class StaticSiteFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticSiteField
        fields = '__all__'


class BulkStaticSiteFieldSerializer(serializers.Serializer):
    fields = serializers.ListField(child=StaticSiteFieldSerializer(), required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError

    @transaction.atomic
    def create(self, validated_data):
        static_site_fields = [StaticSiteField(**data) for data in validated_data['fields']]
        return StaticSiteField.objects.bulk_create(static_site_fields)
