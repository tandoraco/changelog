from rest_framework.routers import DefaultRouter

from v1.categories.views import CategoriesViewset

router = DefaultRouter()
router.register(r'categories', CategoriesViewset)
urlpatterns = router.urls + []
