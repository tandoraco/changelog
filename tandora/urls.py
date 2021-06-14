"""tandora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from frontend.admin import admin_site

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r"api/v1/", include("v1.urls"), name="v1-api"),
    path('admin/', admin_site.urls),
    path('', include('payanpaadu.background_tasks.urls')),
    re_path(r"", include("frontend.urls"), name="v1-frontend"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if (settings.DEBUG or settings.TESTING) and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls), name='djdt'),
    ]
