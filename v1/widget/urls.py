from django.urls import re_path

from v1.widget import views

urlpatterns = [
    re_path(r'^embed-widget/', views.EmbedView.as_view(), name="v1-embed-widget"),
]
