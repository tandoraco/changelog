from django.conf.urls import url
from django.urls import path, include

from frontend.views import auth, app
from frontend.views.core import changelog

urlpatterns = [
    path('', app.ChangeLogList.as_view(), name="frontend-index"),
    url(r'^login', auth.login, name="frontend-login"),
    url(r'^logout', auth.logout, name="frontend-logout"),
    url(r'^app', app.ChangeLogList.as_view(), name="frontend-staff-index"),
    url(r'^changelogs', app.ChangeLogList.as_view(), name="frontend-staff-index"),
    url(r'^create-changelog', changelog.changelog_form, name="frontend-new-changelog"),
    path('edit-changelog/<int:id>', changelog.edit_changelog, name="frontend-edit-changelog"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls'), name='ckeditor'),
    path('changelog/<slug:slug>', app.view_changelog, name="frontend-view-changelog"),
]
