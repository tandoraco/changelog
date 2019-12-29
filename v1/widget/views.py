from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from v1.utils import unprocessable_entity, serializer_error_response
from v1.widget.constants import EMBED_DOES_NOT_EXIST, ONLY_ONE_EMBED_SCRIPT_ALLOWED
from v1.widget.models import Embed
from v1.widget.serializers import EmbedSerializer


class EmbedView(CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = EmbedSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return Embed.objects.filter(company=self.request.user.company)

    def create_or_update_data(self, data, status_code, instance=None):
        data = data.copy()
        data['company'] = self.request.user.company.id

        if not instance:
            serializer = self.serializer_class(data=data)
        else:
            serializer = self.serializer_class(instance=instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status_code, data=serializer.data)
        return serializer_error_response(serializer)

    def list(self, request, *args, **kwargs):

        if self.get_queryset().count() > 0:
            serializer = self.serializer_class(self.get_queryset().first())
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):

        if self.get_queryset().count() > 0:
            return unprocessable_entity(ONLY_ONE_EMBED_SCRIPT_ALLOWED)

        return self.create_or_update_data(request.data, status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):

        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):

        if self.get_queryset().count() > 0:
            instance = self.get_queryset().first()
            return self.create_or_update_data(request.data, status.HTTP_200_OK, instance=instance)

        return unprocessable_entity(EMBED_DOES_NOT_EXIST)
