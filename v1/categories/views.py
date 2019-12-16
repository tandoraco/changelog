from rest_framework.exceptions import ValidationError

from v1.categories.models import Category
from v1.categories.serializers import CategorySerializer
from v1.utils.viewsets import TandoraModelViewSet

ValidationError.status_code = 422


class CategoriesViewSet(TandoraModelViewSet):
    serializer_class = CategorySerializer
    model_class = Category
