# Register your models here.
import csv
from datetime import datetime

from background_task.models import Task, CompletedTask
from django.apps import apps
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from user_visit.models import UserVisit

from frontend.forms.auth import TandoraAdminLoginForm
from v1.audit import models as audit_models
from frontend.views.billing.utils import generate_inr_invoice
from v1.accounts import models as v1_account_models
from v1.accounts.utils import hash_password
from v1.settings.public_page.models import PublicPage


class SyntaxHighlighterMixin:
    class Media:
        js = ('https://tandora-changelog.s3.amazonaws.com/static/js/codemirror.js',
              'https://tandora-changelog.s3.amazonaws.com/static/js/codemirror-css.js',
              'https://tandora-changelog.s3.amazonaws.com/static/js/codemirror-js.js',
              'https://tandora-changelog.s3.amazonaws.com/static/js/codemirror-html-mixed.js',
              'https://tandora-changelog.s3.amazonaws.com/static/js/codemirror-xml.js',
              'https://tandora-changelog.s3.amazonaws.com/static/js/inject-syntax-highlighter.js'
              )
        css = {
            'all': ('css/codemirror.css',)
        }


class ModelAdminWithSyntaxHighlighter(SyntaxHighlighterMixin, admin.ModelAdmin):
    pass


class CompanyAdmin(ModelAdminWithSyntaxHighlighter):
    list_display = ('company_name', 'company_actions',)

    def company_actions(self, obj):
        delete_action_url = reverse('admin-delete-company', args=(obj.company_name,))

        return format_html(
            f'<a class="button" onclick="return confirm(\'Are you sure to delete?\')"href="{delete_action_url}">'
            f'Delete Company</a> &nbsp '
        )

    company_actions.short_description = 'ACTIONS'


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


class CreateDeleteModelAdmin(CreateOnlyModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return True


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


def generate_referral_code_csv(modeladmin, request, queryset):
    codes = queryset.filter(is_used=False).values_list('referral_code', flat=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Tandora Changelog referral codes.csv"'
    writer = csv.writer(response)
    for code in codes:
        writer.writerow([code])
    return response


class ReferralAdmin(admin.ModelAdmin):
    readonly_fields = ('conversion_count', 'company_ids',)
    actions = [generate_referral_code_csv, ]
    search_fields = ('referral_code', )


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
        company = slugify(obj.company.company_name)
        _widget_url = reverse('frontend-public-widget', kwargs={'company': company})
        return format_html(f'<a target="_blank" href="{_widget_url}">{_widget_url}</a>')


class PendingInvoiceAdmin(CreateDeleteModelAdmin):

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        invoice = generate_inr_invoice(plan=data['plan'], company=data['company'])
        obj.invoice_id = invoice['id']
        obj.short_url = invoice['short_url']
        obj.expiry_time = datetime.fromtimestamp(invoice['expire_by'])
        return super(PendingInvoiceAdmin, self).save_model(request, obj, form, change)


admin_site = TandoraLoginAdminSite()
admin_site.register(v1_account_models.Company, CompanyAdmin)
admin_site.register(v1_account_models.User, UserAdmin)
admin_site.register(v1_account_models.PricePlan, ModelAdminWithSyntaxHighlighter)
admin_site.register(v1_account_models.Subscription, SubscriptionAdmin)
admin_site.register(v1_account_models.AngelUser, AngelUserAdmin)
admin_site.register(v1_account_models.Affiliate, CreateReadModelAdmin)
admin_site.register(v1_account_models.Referral, ReferralAdmin)
admin_site.register(v1_account_models.PendingInvoice, PendingInvoiceAdmin)
admin_site.register(v1_account_models.CustomDomain)
admin_site.register(apps.get_model('v1', 'Zapier'), ReadOnlyModelAdmin)
admin_site.register(apps.get_model('v1', 'ZapierWebhookTrigger'), ReadOnlyModelAdmin)
admin_site.register(apps.get_model('v1', 'Webhooks'))
admin_site.register(apps.get_model('v1', 'WebhookLogs'), ReadOnlyModelAdmin)
admin_site.register(apps.get_model('v1', 'Embed'), EmbedWidgetAdmin)
admin_site.register(apps.get_model('v1', 'IncomingWebhook'))
admin_site.register(PublicPage)
admin_site.register(audit_models.AuditLog, ReadOnlyModelAdmin)
admin_site.register(UserVisit, ReadOnlyModelAdmin)
admin_site.register(Task)
admin_site.register(CompletedTask)
