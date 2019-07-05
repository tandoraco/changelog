from django.contrib import messages

from frontend.constants import NOT_LOGGED_IN_ERROR
from v1.accounts.models import ClientToken


def is_valid_auth_token_and_email(request):
    token = request.session.get("auth-token", None)
    email = request.session.get("email", None)

    if not (token or email):
        return False

    try:
        ct = ClientToken.objects.get(token=token)
        assert ct.user.email == email
        assert request.session["user-id"]
    except (ClientToken.DoesNotExist, AssertionError):
        messages.error(request, message=NOT_LOGGED_IN_ERROR)
        return False

    return True
