from django.db import transaction
from rest_framework import serializers
from v1.core.models import Changelog, StaticSiteField


class ChangelogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changelog
        exclude = ('deleted', )
        read_only_fields = ('created_at', 'last_edited_at')


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
