from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin

from frontend.constants import FREE_TRIAL_EXPIRED
from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email, is_trial_expired


class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if is_trial_expired(request):
            messages.error(request, message=FREE_TRIAL_EXPIRED)
            return redirect_to_login(request)

        if not is_valid_auth_token_and_email(request):
            return redirect_to_login(request)

        return super().dispatch(request, *args, **kwargs)


class IsAdmin(LoginRequiredMixin, PermissionRequiredMixin):

    def has_permission(self):
        return self.request.user.company.admin == self.request.user
