from rest_framework.exceptions import MethodNotAllowed

from v1.settings.public_page.models import PublicPage
from v1.settings.public_page.serializers import PublicPageSerializer
from v1.utils.viewsets import TandoraModelViewSet


class PublicPageViewSet(TandoraModelViewSet):
    queryset = PublicPage.objects.all()
    serializer_class = PublicPageSerializer

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
