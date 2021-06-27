from django.urls import re_path

from v1.static_site import views

urlpatterns = [
    re_path(r'static-site-fields/', views.bulk_create_static_site_fields_from_json,
            name='v1-bulk-create-static-site-fields-json')
]
