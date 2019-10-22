from django.contrib.auth.mixins import AccessMixin

from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email


class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not is_valid_auth_token_and_email(request):
            return redirect_to_login(request)

        return super().dispatch(request, *args, **kwargs)
