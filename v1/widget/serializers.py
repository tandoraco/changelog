from rest_framework.serializers import ModelSerializer

from v1.utils.validators import validate_color
from v1.widget.models import Embed


class EmbedSerializer(ModelSerializer):

    class Meta:
        model = Embed
        exclude = ('id', )

    def validate_color(self, color):
        return validate_color(color)
