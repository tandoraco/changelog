import functools

from django.http import HttpResponseRedirect

from v1.accounts.models import ClientToken


def check_auth(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        token = request.session["auth-token"]
        email = request.session["email"]

        try:
            ct = ClientToken.objects.get(token=token)
            assert ct.user.email == email
            assert request.session["user-id"]
        except (ClientToken.DoesNotExist, AssertionError):
            return HttpResponseRedirect("/login")

        return func(*args, **kwargs)

    return wrapper
