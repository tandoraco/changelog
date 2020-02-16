from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import RedirectView

from frontend.sitemaps import SITEMAPS
from frontend.views import auth, app, categories, widget, static_site, integrations, settings
from frontend.views.core import changelog

urlpatterns = [
    path('', RedirectView.as_view(url='staff'), name="frontend-index"),
    url(r'^login', auth.login, name="frontend-login"),
    url(r'^logout', auth.logout, name="frontend-logout"),
    url(r'^signup', auth.signup, name="frontend-signup"),
    url(r'^affiliate-signup', auth.affiliate_signup, name="frontend-affiliate-signup"),
    url(r'^forgot-password', auth.forgot_password_form, name="frontend-forgot-password"),
    url(r'^reset-password/(?P<token>[0-9A-Fa-f-]+)', auth.reset_password_form, name="frontend-reset-password"),
    url(r'^verify-user/(?P<token>[0-9A-Fa-f-]+)', auth.verify_user, name='frontend-verify-user'),
    path('webhook/razorpay', auth.razorpay_webhook, name="razorpay-webhook"),
    path('staff', app.ChangeLogList.as_view(), name="frontend-staff-index"),
    path('staff/create-changelog', changelog.changelog_form, name="frontend-create-changelog"),
    path('staff/edit-changelog/<int:id>', changelog.edit_changelog, name="frontend-edit-changelog"),
    path('staff/delete-changelog/<int:id>', changelog.delete_changelog, name="frontend-delete-changelog"),
    path('staff/changelog/<slug:slug>', app.view_changelog, name="frontend-view-changelog"),
    path('staff/create-page', changelog.changelog_form, name="frontend-create-page"),
    path('staff/edit-page/<int:id>', changelog.edit_changelog, name="frontend-edit-page"),
    path('staff/delete-page/<int:id>', changelog.delete_changelog, name="frontend-delete-page"),
    path('staff/page/<slug:slug>', app.view_changelog, name="frontend-view-page"),
    path('staff/manage/users', app.UserList.as_view(), name="frontend-view-users"),
    path('staff/manage/users/create-user', app.create_user, name="frontend-create-user"),
    path('staff/manage/users/edit-user/<int:id>', app.edit_user, name="frontend-edit-user"),
    path('staff/manage/users/deactivate-user/<int:id>', app.deactivate_user, name="frontend-deactivate-user"),
    path('staff/manage/users/activate-user/<int:id>', app.activate_user, name="frontend-activate-user"),
    path('staff/manage/users/reset-password/<int:id>', app.reset_password, name="frontend-admin-reset-password"),
    path('staff/manage/categories', categories.CategoryList.as_view(), name="frontend-view-categories"),
    path('staff/manage/categories/create-category', categories.category_form, name="frontend-create-category"),
    path('staff/manage/categories/edit-category/<int:id>', categories.edit_category, name="frontend-edit-category"),
    path('staff/manage/categories/delete-category/<int:id>', categories.delete_category,
         name="frontend-delete-category"),
    path('staff/manage/integrations', integrations.IntegrationList.as_view(), name="frontend-view-integrations"),
    path('staff/manage/integrations/<str:integration>', integrations.integration_form,
         name="frontend-edit-integrations"),
    path('staff/manage/profile/company', auth.company_form, name="frontend-company-form"),
    path('staff/manage/profile/myself', auth.profile_form, name="frontend-profile-form"),
    path('staff/manage/widget', widget.widget_form, name="frontend-manage-widget"),
    path('staff/manage/theme', static_site.theme_form, name="frontend-manage-theme"),
    path('staff/manage/static-site', static_site.static_site_form, name="frontend-manage-static-site"),
    path('staff/manage/public-page', settings.manage_public_page, name="frontend-manage-public-page"),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    path('<str:company>', app.company_public_index, name="frontend-company-public-index"),
    path('<str:company>/<str:changelog_terminology>/widget/1', widget.public_widget, name="frontend-public-widget"),
    path('<str:company>/<str:changelog_terminology>/<slug:slug>', app.view_changelog_as_public,
         name="frontend-view-changelog-as-public"),
    path('<str:company>/<str:changelog_terminology>', app.public_index, name="frontend-public-index"),
]
