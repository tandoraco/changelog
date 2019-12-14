from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from v1.core.views import ChangelogViewSet, bulk_create_static_site_fields_from_json

router = DefaultRouter()
router.register(r'changelogs', ChangelogViewSet)
urlpatterns = router.urls + [
    url(r'static-site-fields/', bulk_create_static_site_fields_from_json,
        name='v1-bulk-create-static-site-fields-json')
]
