from rest_framework.exceptions import PermissionDenied

from v1.settings.public_page.models import PublicPage
from v1.settings.public_page.serializers import PublicPageSerializer
from v1.utils.viewsets import TandoraModelViewset


class PublicPageViewset(TandoraModelViewset):
    queryset = PublicPage.objects.all()
    serializer_class = PublicPageSerializer

    def create(self, request, *args, **kwargs):
        raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied
