from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from frontend.views import auth, app, categories, widget
from frontend.views.core import changelog

urlpatterns = [
    path('', RedirectView.as_view(url='staff/changelogs'), name="frontend-index"),
    url(r'^login', auth.login, name="frontend-login"),
    url(r'^logout', auth.logout, name="frontend-logout"),
    url(r'^forgot-password', auth.forgot_password_form, name="frontend-forgot-password"),
    url(r'^reset-password/(?P<token>[0-9A-Fa-f-]+)', auth.reset_password_form, name="frontend-reset-password"),
    path('webhook/razorpay', auth.razorpay_webhook, name="razorpay-webhook"),
    path('staff/changelogs', app.ChangeLogList.as_view(), name="frontend-staff-index"),
    path('staff/create-changelog', changelog.changelog_form, name="frontend-new-changelog"),
    path('staff/edit-changelog/<int:id>', changelog.edit_changelog, name="frontend-edit-changelog"),
    path('staff/delete-changelog/<int:id>', changelog.delete_changelog, name="frontend-delete-changelog"),
    path('staff/changelog/<slug:slug>', app.view_changelog, name="frontend-view-changelog"),
    path('staff/manage/categories', categories.CategoryList.as_view(), name="frontend-view-categories"),
    path('staff/manage/categories/create-category', categories.category_form, name="frontend-category-form"),
    path('staff/manage/categories/edit-category/<int:id>', categories.edit_category, name="frontend-edit-category"),
    path('staff/manage/categories/delete-category/<int:id>', categories.delete_category,
         name="frontend-delete-category"),
    path('staff/manage/profile/company', auth.company_form, name="frontend-company-form"),
    path('staff/manage/profile/myself', auth.profile_form, name="frontend-profile-form"),
    path('staff/manage/widget', widget.widget_form, name="frontend-manage-widget"),
    path('<str:company>/<str:changelog_terminology>/widget/1', widget.public_widget, name="frontend-public-widget"),
    path('<str:company>/<str:changelog_terminology>/<slug:slug>', app.view_changelog_as_public,
         name="frontend-view-changelog-as-public"),
    path('<str:company>/<str:changelog_terminology>', app.public_index, name="frontend-public-index"),
]
