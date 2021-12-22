from django.urls import path

from v1.audit.views import record_public_page_view

urlpatterns = [
    path('public-page-view/', record_public_page_view, name='v1-record-public-page-view'),
]
