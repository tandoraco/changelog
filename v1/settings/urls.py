from django.conf.urls import include
from django.urls import path, re_path

from v1.settings import views

urlpatterns = [
    path(r'', include('v1.settings.public_page.urls')),
    re_path(r'settings/', views.settings, name='v1-settings'),
]
