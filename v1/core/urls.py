from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from v1.core import views

router = DefaultRouter()
router.register(r'changelogs', views.ChangelogViewSet, basename='changelogs')

urlpatterns = router.urls + [
    re_path(r'inline-image/', views.inline_image_attachment, name='v1-inline-image'),
    path('view-count/<int:pk>/', views.increase_view_count, name='v1-view-count'),
]
