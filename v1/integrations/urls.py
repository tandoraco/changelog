from django.urls import path

from v1.integrations import views

urlpatterns = [
    path('integrations/<str:integration_name>/', views.integration_settings, name='integration-settings'),
    path('integrations/<str:integration_name>/<str:action>/', views.integration_action, name='integration-action'),
]
