from rest_framework.routers import DefaultRouter

from v1.core.views import ChangelogViewset

router = DefaultRouter()
router.register(r'changelogs', ChangelogViewset)
urlpatterns = router.urls + []
