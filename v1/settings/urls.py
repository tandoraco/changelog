from django.conf.urls import include, url
from django.urls import path

from v1.settings import views

urlpatterns = [
    path(r'', include('v1.settings.public_page.urls')),
    url(r'settings/', views.settings, name='v1-settings'),
]
