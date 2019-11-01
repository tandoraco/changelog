# Register your models here.
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext as _

from frontend.forms.auth import TandoraAdminLoginForm
from v1.accounts.models import Company, User, Subscription, PricePlan
from v1.accounts.utils import hash_password


class TandoraLoginAdminSite(AdminSite):
    site_title = _('Tandora Admin')
    site_header = _('Tandora')
    index_title = _('Login')
    login_form = TandoraAdminLoginForm


class UserAdmin(admin.ModelAdmin):
    exclude = ['password_hash', 'last_login']

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password_hash = hash_password(obj.password)
            obj.password = ''

        obj.save()


admin_site = TandoraLoginAdminSite()
admin_site.register(Company)
admin_site.register(User, UserAdmin)
admin_site.register(PricePlan)
admin_site.register(Subscription)
