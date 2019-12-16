from rest_framework.routers import DefaultRouter

from v1.settings.public_page.views import PublicPageViewSet

router = DefaultRouter()
router.register(r'settings/public-page', PublicPageViewSet, basename='settings-public-page')
urlpatterns = router.urls + []
