from django.conf import settings as django_settings
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
from django.views.generic import RedirectView

from frontend.sitemaps import SITEMAPS
from frontend.views import auth, app, categories, widget, integrations, settings, admin_actions, billing
from frontend.views.integrations import slack
from frontend.views.core import changelog
from frontend.views.rss import PublicChangelogFeed

urlpatterns = [
    path('', RedirectView.as_view(url='staff'), name="frontend-index"),
    re_path(r'^login/?$', auth.login, name="frontend-login"),
    re_path(r'^logout/?$', auth.logout, name="frontend-logout"),
    re_path(r'^signup/?$', auth.signup, name="frontend-signup"),
    re_path(r'^affiliate-signup/?$', auth.affiliate_signup, name="frontend-affiliate-signup"),
    re_path(r'^forgot-password/?$', auth.forgot_password_form, name="frontend-forgot-password"),
    re_path(r'^reset-password/(?P<token>[0-9A-Fa-f-]+)/?$', auth.reset_password_form, name="frontend-reset-password"),
    re_path(r'^verify-user/(?P<token>[0-9A-Fa-f-]+)/?$', auth.verify_user, name='frontend-verify-user'),
    re_path(r'^webhook/razorpay/?$', auth.razorpay_webhook, name="razorpay-webhook"),
    path('staff', app.ChangeLogList.as_view(), name="frontend-staff-index"),
    path('staff/billing', billing.billing_page, name='frontend-billing-page'),
    path('staff/create-changelog', changelog.create_changelog, name="frontend-create-changelog"),
    path('staff/edit-changelog/<int:id>', changelog.edit_changelog, name="frontend-edit-changelog"),
    path('staff/delete-changelog/<int:id>', changelog.delete_changelog, name="frontend-delete-changelog"),
    path('staff/changelog/<slug:slug>', app.view_changelog, name="frontend-view-changelog"),
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
    path('staff/manage/integrations/<str:integration>/embed', integrations.embed_details,
         name="frontend-integrations-embed"),
    path('staff/slack/oauth/start', slack.oauth_start, name='slack-oauth-start'),
    path('slack/oauth/callback', slack.oauth_callback, name='slack-oauth-callback'),
    path('staff/manage/profile/company', auth.company_form, name="frontend-company-form"),
    path('staff/manage/profile/myself', auth.profile_form, name="frontend-profile-form"),
    path('staff/manage/widget', widget.widget_form, name="frontend-manage-widget"),
    path('staff/manage/public-page', settings.manage_public_page, name="frontend-manage-public-page"),
    path('staff/admin/actions/delete-company/<str:company_name>', admin_actions.delete_company,
         name='admin-delete-company'),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    path('<str:company>', app.company_public_index, name="frontend-company-public-index"),
    # Removing previous widget url because, widget url was dependant on company name and terminology
    # if terminology changes the widget url will also change, this wont be feasible in the long run
    # because we cannot ask our customers to change the widget url often, since they
    # would have embedded their widget. so defining a new widget url
    # and hard-coding the production users widget url for backwards compatibility
    path('<str:company>/<str:changelog_terminology>/widget/1', widget.legacy_widget, name="frontend-legacy-widget"),
    path('widget/<str:company>', widget.public_widget, name="frontend-public-widget"),
    path('<str:company>/<str:changelog_terminology>/rss', PublicChangelogFeed(), name='public-rss-feed'),
    path('<str:company>/<str:changelog_terminology>/<slug:slug>', app.view_changelog_as_public,
         name="frontend-view-changelog-as-public"),
    path('<str:company>/<str:changelog_terminology>', app.public_index, name="frontend-public-index"),
]

if not django_settings.DEBUG:
    # This is to prevent debug tool bar not getting rendered during development.
    urlpatterns += [
        # re_path(r'^.*/$', app.view_changelog_custom_url, name='frontend-view-changelog-custom-url'),
    ]
