import random

from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers

from v1.core.models import Changelog, InlineImageAttachment
from v1.utils import html_2_text, extract_all_image_src_urls


class ChangelogSerializer(serializers.ModelSerializer):
    custom_url_path = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Changelog
        exclude = ('deleted',)
        read_only_fields = ('created_at', 'last_edited_at')

    def validate_custom_url_path(self, custom_url_path):
        if custom_url_path and (custom_url_path.startswith('/') or custom_url_path.endswith('/')):
            return custom_url_path.strip('/')
        return custom_url_path


class ChangelogSerializerForZapier(ChangelogSerializer):

    def to_representation(self, instance):
        all_images = extract_all_image_src_urls(instance.content)
        company_name = slugify(instance.company.company_name)
        terminology = slugify(instance.company.changelog_terminology)
        return {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'content_text': html_2_text(instance.content),
            'images': all_images,
            'random_image': random.choice(all_images) if all_images else '',
            'view_url': f'{settings.HOST}{company_name}/{terminology}/{instance.slug}'
        }


class InlineImageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineImageAttachment
        exclude = ('created_at',)
