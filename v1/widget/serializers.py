from rest_framework.serializers import ModelSerializer

from v1.utils.validators import validate_color
from v1.widget.models import Embed


class EmbedSerializer(ModelSerializer):

    class Meta:
        model = Embed
        fields = '__all__'

    def validate_color(self, color):
        return validate_color(color)

    def to_representation(self, instance):
        return {
            'html': instance.get_default_embed_script(),
            'color': instance.color
        }
