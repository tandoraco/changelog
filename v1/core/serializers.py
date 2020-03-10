from rest_framework import serializers

from v1.core.models import Changelog, InlineImageAttachment


class ChangelogSerializer(serializers.ModelSerializer):
    custom_url_path = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Changelog
        exclude = ('deleted', )
        read_only_fields = ('created_at', 'last_edited_at')

    def validate_custom_url_path(self, custom_url_path):
        if custom_url_path and (custom_url_path.startswith('/') or custom_url_path.endswith('/')):
            return custom_url_path.strip('/')
        return custom_url_path


class InlineImageAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = InlineImageAttachment
        exclude = ('created_at', )
