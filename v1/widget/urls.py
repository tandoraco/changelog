from django.conf.urls import url

from v1.widget import views

urlpatterns = [
    url(r'^embed-widget/', views.EmbedView.as_view(), name="v1-embed-widget"),
]
