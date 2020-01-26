from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from v1.core.views import ChangelogViewSet, inline_image_attachment

router = DefaultRouter()
router.register(r'changelogs', ChangelogViewSet, basename='changelogs')

urlpatterns = router.urls + [
    url(r'inline-image/', inline_image_attachment, name='v1-inline-image'),
]
