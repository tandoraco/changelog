from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from v1.utils import unprocessable_entity, serializer_error_response
from v1.widget.constants import EMBED_DOES_NOT_EXIST, ONLY_ONE_EMBED_SCRIPT_ALLOWED
from v1.widget.models import Embed
from v1.widget.serializers import EmbedSerializer


class EmbedView(CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = EmbedSerializer
    queryset = Embed.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def _create_and_return_data(self, data, status_code):

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status_code, data=serializer.data)
        return serializer_error_response(serializer)

    def list(self, request, *args, **kwargs):

        if self.queryset.count() > 0:
            serializer = self.serializer_class(self.queryset.first())
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):

        if self.queryset.count() > 0:
            return unprocessable_entity(ONLY_ONE_EMBED_SCRIPT_ALLOWED)

        return self._create_and_return_data(request.data, status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):

        self.queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):

        # Since only one embed script can exist for an account, whenever we want to update
        # we delete the old one and create new embed script.
        # this is a bit of hack, since we do not want to expost primary key in endpoint
        if self.queryset.count() > 0:
            self.queryset.delete()
            return self._create_and_return_data(request.data, status.HTTP_200_OK)

        return unprocessable_entity(EMBED_DOES_NOT_EXIST)
