from v1.core.models import Changelog
from v1.core.serializers import ChangelogSerializer
from v1.utils.viewsets import TandoraModelViewSet


class ChangelogViewSet(TandoraModelViewSet):
    queryset = Changelog.objects.all()
    serializer_class = ChangelogSerializer

    def create(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk
        return super(ChangelogViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk

        return super(ChangelogViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk

        return super(ChangelogViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk
            request.data["deleted"] = True

        return super(ChangelogViewSet, self).destroy(request, *args, **kwargs)
