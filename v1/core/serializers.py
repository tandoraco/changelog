import random

from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers

from v1.core.models import Changelog, InlineImageAttachment
from v1.integrations.background_tasks import trigger_integration_background_tasks
from v1.utils import html_2_text, extract_all_image_src_urls


class ChangelogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changelog
        exclude = ('deleted',)
        read_only_fields = ('created_at', 'last_edited_at')

    @property
    def custom_full_errors_str(self):
        """
        Returns full errors formatted as per requirements
        """
        default_errors = self.errors  # default errors dict
        errors_messages = []
        for field_name, field_errors in default_errors.items():
            for field_error in field_errors:
                error_message = '%s: %s' % (field_name.title(), field_error)
                errors_messages.append(error_message)  # append error message to 'errors_messages'
        return '\n'.join(errors_messages)

    def create(self, validated_data):
        changelog = super(ChangelogSerializer, self).create(validated_data)
        trigger_integration_background_tasks(changelog.company.id, changelog.id, **{'created': True})
        return changelog

    def update(self, instance, validated_data):
        changelog = super(ChangelogSerializer, self).update(instance, validated_data)
        trigger_integration_background_tasks(changelog.company.id, changelog.id, **{'created': False})
        return changelog


class ChangelogSerializerForZapier(ChangelogSerializer):

    def to_representation(self, instance):
        all_images = extract_all_image_src_urls(instance.content)
        company_name = slugify(instance.company.company_name)
        terminology = slugify(instance.company.changelog_terminology)
        auto_append_content = instance.auto_append_content
        return {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'content_text': html_2_text(instance.content),
            'auto_append_content': auto_append_content,
            'auto_append_content_text': html_2_text(auto_append_content),
            'images': all_images,
            'random_image': random.choice(all_images) if all_images else '',
            'featured_image': instance.featured_image.url if instance.featured_image else None,
            'view_url': f'{settings.HOST}{company_name}/{terminology}/{instance.slug}',
            'created_at': instance.created_at,
            'last_edited_at': instance.last_edited_at
        }


class InlineImageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineImageAttachment
        exclude = ('created_at',)
