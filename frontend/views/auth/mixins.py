from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin

from frontend.constants import FREE_TRIAL_EXPIRED, LOGIN_AGAIN_INFO
from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email, is_trial_expired
from v1.accounts.models import ClientToken


class LoginRequiredMixin(AccessMixin):
    admin_id = None

    def dispatch(self, request, *args, **kwargs):
        company = None

        try:
            token = ClientToken.objects.filter(token=request.session['auth-token']).\
                select_related('user__company', 'user__company__admin')[0]
            company = token.user.company
            self.admin_id = token.user.company.admin.id
        except (KeyError, IndexError):
            messages.info(request, message=LOGIN_AGAIN_INFO, fail_silently=True)
            return redirect_to_login(request)

        if is_trial_expired(request, company):
            messages.error(request, message=FREE_TRIAL_EXPIRED)
            return redirect_to_login(request)

        if not is_valid_auth_token_and_email(request, company, ct=token):
            return redirect_to_login(request)

        return super().dispatch(request, *args, **kwargs)


class IsAdmin(LoginRequiredMixin, PermissionRequiredMixin):

    def has_permission(self):
        return self.admin_id == self.request.user.id
