from django.urls import path

from v1.links.views import track_link_click

urlpatterns = [
    path('track-link-click/<int:pk>/', track_link_click, name='v1-track-link-click'),
]
