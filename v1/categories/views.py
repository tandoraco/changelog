from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from v1.categories.models import Category
from v1.categories.serializers import CategorySerializer

ValidationError.status_code = 422


class CategoriesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
