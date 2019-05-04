from rest_framework.routers import DefaultRouter

from v1.settings.public_page.views import PublicPageViewset

router = DefaultRouter()
router.register(r'settings/public-page', PublicPageViewset)
urlpatterns = router.urls + []
