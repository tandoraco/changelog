from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(r'', include('v1.settings.public_page.urls')),
]
