from v1.core.models import Changelog
from v1.core.serializers import ChangelogSerializer
from v1.utils.viewsets import TandoraModelViewSet


class ChangelogViewSet(TandoraModelViewSet):
    serializer_class = ChangelogSerializer
    model_class = Changelog
