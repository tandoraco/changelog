from django.conf.urls import url
from knox import views as knox_views

from v1.accounts import views

urlpatterns = [
    url(r'login/', views.LoginView.as_view(), name='knox-login'),
    url(r'logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    url(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox-logoutall'),
    url(r'^create-company/$', views.create_company, name="v1-admin-and-company"),
    url(r'^create-user/$', views.create_user, name="v1-create-user"),
]
