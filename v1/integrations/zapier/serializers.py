from rest_framework import serializers

from v1.integrations.zapier.models import Zapier


class ZapierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zapier
        exclude = ('id', 'company', )
