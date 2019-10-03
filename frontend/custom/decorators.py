import functools

from django.http import HttpResponseRedirect

from frontend.forms.auth.utils import is_valid_auth_token_and_email


def is_authenticated(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        if not is_valid_auth_token_and_email(request):
            return HttpResponseRedirect("/login")

        return func(*args, **kwargs)

    return wrapper
