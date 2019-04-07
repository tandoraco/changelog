from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def verify_password(user, password):
    try:
        hasher = PasswordHasher()
        return hasher.verify(
            user.password_hash, password)
    except VerifyMismatchError:
        return False


def hash_password(password):
    return PasswordHasher().hash(password)
