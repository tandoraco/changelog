from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from v1.accounts.constants import EMAIL_OR_PASSWORD_INVALID
from v1.accounts.models import User
from v1.accounts.serializers import LoginSerializer


class BasicAuthentication(BaseAuthentication):
    """ knox library is used to generate tokens and verify them.

    We do not store password in db. Only password hash is stored. But knox expects a password.
    So this class verifies whether a password provided matches with the hash in the db.
    This class will be used by knox to validate a user and generated token.
    Reference: https://james1345.github.io/django-rest-knox/auth/
    """

    def authenticate(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data["email"])
            return user, user.email
        else:
            raise AuthenticationFailed(EMAIL_OR_PASSWORD_INVALID)
