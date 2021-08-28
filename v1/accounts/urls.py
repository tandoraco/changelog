from django.urls import re_path
from knox import views as knox_views

from v1.accounts import views

urlpatterns = [
    re_path(r'login/', views.LoginView.as_view(), name='knox-login'),
    re_path(r'logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    re_path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox-logoutall'),
    re_path(r'^create-company/$', views.create_company, name="v1-admin-and-company"),
    re_path(r'^create-user/$', views.create_user, name="v1-create-user"),
    re_path(r'^forgot-password/$', views.forgot_password, name="v1-forgot-password"),
    re_path(r'^reset-password/(?P<token>[0-9A-Fa-f-]+)', views.reset_password, name="v1-reset-password"),
]
