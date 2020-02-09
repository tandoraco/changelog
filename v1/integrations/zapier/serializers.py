from rest_framework import serializers

from v1.integrations.zapier.models import Zapier

INVALID_API_KEY = 'Zapier API key is invalid.'


class ZapierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zapier
        exclude = ('id', 'company', )


class ZapierApiKeySerializer(serializers.Serializer):
    api_key = serializers.UUIDField(required=True)

    def validate_api_key(self, api_key):
        try:
            Zapier.objects.get(api_key=api_key)
        except Zapier.DoesNotExist:
            raise serializers.ValidationError(INVALID_API_KEY)

        return api_key
