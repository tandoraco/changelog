from rest_framework import serializers

from v1.core.models import Changelog


class ChangelogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changelog
        exclude = ('deleted', )
        read_only_fields = ('created_at', 'last_edited_at')
