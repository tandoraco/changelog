from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from v1.categories.models import Category
from v1.categories.serializers import CategorySerializer


class CategoriesViewset(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated, )
