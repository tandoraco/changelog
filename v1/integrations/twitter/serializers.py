from rest_framework import serializers

from v1.integrations.twitter.models import Twitter


class TwitterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Twitter
        exclude = ('company', )
