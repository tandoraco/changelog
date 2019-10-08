from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from django.contrib.auth.base_user import BaseUserManager


def verify_password(user, password):
    try:
        hasher = PasswordHasher()
        return hasher.verify(
            user.password_hash, password)
    except VerifyMismatchError:
        return False


def hash_password(password):
    return PasswordHasher().hash(password)


class UserManager(BaseUserManager):

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})
