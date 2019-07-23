from django.conf.urls import url
from django.urls import path

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
    path('delete-changelog/<int:id>', changelog.delete_changelog, name="frontend-delete-changelog"),
    path('changelog/<slug:slug>', app.view_changelog, name="frontend-view-changelog"),
    path('<str:company>/<str:changelog_terminology>/<slug:slug>', app.view_changelog_as_public,
         name="frontend-view-changelog-as-public"),
    path('<str:company>/<str:changelog_terminology>', app.public_index, name="frontend-public-index"),
]
