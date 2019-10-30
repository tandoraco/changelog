import functools

from django.contrib import messages

from frontend.constants import FREE_TRIAL_EXPIRED
from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email, is_trial_expired


def is_authenticated(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        if is_trial_expired(request):
            messages.error(request, message=FREE_TRIAL_EXPIRED)
            return redirect_to_login(request)

        if not is_valid_auth_token_and_email(request):
            return redirect_to_login(request)

        return func(*args, **kwargs)

    return wrapper
