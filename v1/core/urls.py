from rest_framework.routers import DefaultRouter

from v1.core.views import ChangelogViewSet

router = DefaultRouter()
router.register(r'changelogs', ChangelogViewSet, basename='changelogs')

urlpatterns = router.urls + []
