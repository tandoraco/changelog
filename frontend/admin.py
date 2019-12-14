# Register your models here.
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext as _

from frontend.forms.auth import TandoraAdminLoginForm
from v1.accounts import models as v1_account_models
from v1.core import models as v1_core_models
from v1.accounts.utils import hash_password


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


class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('razorpay_data', )


class ReferralAdmin(admin.ModelAdmin):
    readonly_fields = ('conversion_count', 'company_ids', )


admin_site = TandoraLoginAdminSite()
admin_site.register(v1_account_models.Company)
admin_site.register(v1_account_models.User, UserAdmin)
admin_site.register(v1_account_models.PricePlan)
admin_site.register(v1_account_models.Subscription, SubscriptionAdmin)
admin_site.register(v1_account_models.AngelUser, AngelUserAdmin)
admin_site.register(v1_account_models.Affiliate)
admin_site.register(v1_account_models.Referral, ReferralAdmin)
admin_site.register(v1_account_models.CustomDomain)
admin_site.register(v1_core_models.StaticSiteTheme)
admin_site.register(v1_core_models.StaticSiteField, CreateUpdateModelAdmin)
admin_site.register(v1_core_models.StaticSiteThemeConfig, CreateOnlyModelAdmin)
