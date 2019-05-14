from rest_framework.routers import DefaultRouter

from v1.core.views import ChangelogViewSet

router = DefaultRouter()
router.register(r'changelogs', ChangelogViewSet)
urlpatterns = router.urls + []
