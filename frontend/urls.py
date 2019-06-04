from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from frontend.views import auth

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    url(r'^login', auth.login, name="frontend-login"),
]
