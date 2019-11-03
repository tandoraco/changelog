# Register your models here.
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext as _

from frontend.forms.auth import TandoraAdminLoginForm
from v1.accounts.models import Company, User, Subscription, PricePlan, AngelUser
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


admin_site = TandoraLoginAdminSite()
admin_site.register(Company)
admin_site.register(User, UserAdmin)
admin_site.register(PricePlan)
admin_site.register(Subscription, SubscriptionAdmin)
admin_site.register(AngelUser, AngelUserAdmin)
