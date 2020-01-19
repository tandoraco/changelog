from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

ValidationError.status_code = 422


class TandoraModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def _is_test(self, kwargs):
        return kwargs.get("test", False)

    def get_queryset(self):
        if hasattr(self.model_class, 'deleted'):
            return self.model_class.objects\
                .filter(company=self.request.user.company, deleted=False)\
                .order_by('id')
        else:
            return self.model_class.objects.\
                filter(company=self.request.user.company).\
                order_by('id')

    def create(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data['created_by'] = request.user.pk
            request.data["last_edited_by"] = request.user.pk
            request.data['company'] = request.user.company.id

        return super(TandoraModelViewSet, self).create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data["last_edited_by"] = request.user.pk
            request.data['company'] = request.user.company.id

        return super(TandoraModelViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_test(kwargs):
            request.data['company'] = request.user.company.id
            if hasattr(self.model_class, 'deleted'):
                request.data['deleted'] = True

        return super(TandoraModelViewSet, self).destroy(request, *args, **kwargs)
