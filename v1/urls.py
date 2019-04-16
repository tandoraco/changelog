from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path(r'', include('v1.accounts.urls')),
    path(r'', include('v1.categories.urls')),
    path(r'', include('v1.core.urls')),
]
