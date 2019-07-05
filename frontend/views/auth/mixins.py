from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect

from frontend.forms.auth.utils import is_valid_auth_token_and_email


class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not is_valid_auth_token_and_email(request):
            return HttpResponseRedirect("/login")

        return super().dispatch(request, *args, **kwargs)
