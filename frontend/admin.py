# Register your models here.
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from frontend.forms.auth import TandoraAdminLoginForm
from v1.accounts import models as v1_account_models
from v1.accounts.utils import hash_password
from v1.static_site import models as v1_static_site_models


class SyntaxHighlighterMixin:
    class Media:
        js = ('js/codemirror.js',
              'js/codemirror-css.js',
              'js/codemirror-js.js',
              'js/codemirror-html-mixed.js',
              'js/codemirror-xml.js',
              'js/inject-syntax-highlighter.js'
              )
        css = {
            'all': ('css/codemirror.css',)
        }


class ModelAdminWithSyntaxHighlighter(SyntaxHighlighterMixin, admin.ModelAdmin):
    pass


class TandoraLoginAdminSite(AdminSite):
    site_title = _('Tandora Admin')
    site_header = _('Tandora')
    index_title = _('Login')
    login_form = TandoraAdminLoginForm


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CreateReadModelAdmin(ReadOnlyModelAdmin):

    def has_add_permission(self, request):
        return True


class CreateOnlyModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CreateUpdateModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(admin.ModelAdmin):
    exclude = ['password_hash', 'last_login']

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password_hash = hash_password(obj.password)
            obj.password = ''

        obj.save()


class AngelUserAdmin(ReadOnlyModelAdmin):
    fieldsets = [
        (None, {'fields': ['email']}),
        ('JSON', {'fields': ['data_formatted']}),
    ]
    readonly_fields = ('data', 'data_formatted')


class SubscriptionAdmin(SyntaxHighlighterMixin, admin.ModelAdmin):
    readonly_fields = ('razorpay_data',)


class ReferralAdmin(admin.ModelAdmin):
    readonly_fields = ('conversion_count', 'company_ids',)


class ChangelogAdmin(admin.ModelAdmin):
    readonly_fields = (
        'company',
        'title',
        'slug',
        'content',
        'category',
        'published',
        'created_by',
        'last_edited_at',
        'last_edited_by',
        'view_count',
        'deleted'
    )
    fields = ('created_at',)
    search_fields = ('pk', 'id', 'title', 'content')
    list_per_page = 25
    list_display = ('id', 'company', 'title',)
    list_filter = ('company', 'deleted', 'created_at', 'view_count',)


class EmbedWidgetAdmin(ModelAdminWithSyntaxHighlighter):
    list_display = ('company', 'enabled', 'widget_url')

    def widget_url(self, obj):
        company_name = slugify(obj.company.company_name)
        changelog_terminology = slugify(obj.company.changelog_terminology)
        _widget_url = f'{settings.HOST}{company_name}/{changelog_terminology}/widget/1'
        return format_html(f'<a target="_blank" href="{_widget_url}">{_widget_url}</a>')


admin_site = TandoraLoginAdminSite()
admin_site.register(v1_account_models.Company, ModelAdminWithSyntaxHighlighter)
admin_site.register(v1_account_models.User, UserAdmin)
admin_site.register(v1_account_models.PricePlan, ModelAdminWithSyntaxHighlighter)
admin_site.register(v1_account_models.Subscription, SubscriptionAdmin)
admin_site.register(v1_account_models.AngelUser, AngelUserAdmin)
admin_site.register(v1_account_models.Affiliate, CreateReadModelAdmin)
admin_site.register(v1_account_models.Referral, ReferralAdmin)
admin_site.register(v1_account_models.CustomDomain)
admin_site.register(v1_static_site_models.StaticSiteTheme, ModelAdminWithSyntaxHighlighter)
admin_site.register(v1_static_site_models.StaticSiteField, CreateUpdateModelAdmin)
admin_site.register(v1_static_site_models.StaticSiteThemeConfig, CreateUpdateModelAdmin)
admin_site.register(apps.get_model('v1', 'Zapier'), ReadOnlyModelAdmin)
admin_site.register(apps.get_model('v1', 'ZapierWebhookTrigger'), ReadOnlyModelAdmin)
admin_site.register(apps.get_model('v1', 'Embed'), EmbedWidgetAdmin)
