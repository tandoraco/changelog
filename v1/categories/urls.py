from rest_framework.routers import DefaultRouter

from v1.categories.views import CategoriesViewSet

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
urlpatterns = router.urls + []
