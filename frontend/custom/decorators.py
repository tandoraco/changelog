import functools

from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email


def is_authenticated(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        if not is_valid_auth_token_and_email(request):
            return redirect_to_login(request)

        return func(*args, **kwargs)

    return wrapper
