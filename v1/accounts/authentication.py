from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from v1.accounts.constants import EMAIL_OR_PASSWORD_INVALID
from v1.accounts.models import User, ClientToken
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


class FrontEndTokenAuthentication(BasicAuthentication):

    def authenticate(self, request):
        token = request.session.get("auth-token", None)
        email = request.session.get("email", None)

        if not (token or email):
            # I am returning None here, because when authentication classes are chained,
            # DRF expects to return None for chained authentication classes to be called.
            # I am planning to use this class with TokenAuthentication in inline-image api
            return None

        try:
            ct = ClientToken.objects.get(token=token)
            assert ct.user.email == email

            if not ct.user.is_active:
                return None

            return ct.user, ct.user.email
        except (ClientToken.DoesNotExist, AssertionError):
            return None
