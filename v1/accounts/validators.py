import string

from rest_framework.serializers import ValidationError

from v1.accounts.constants import (PASSWORD_CONSTRAINS_NOT_MET,
                                   PASSWORD_LENGTH_VALIDATION_FAILED,
                                   MIN_PASSWORD_LENGTH,
                                   MAX_PASSWORD_LENGTH)

LOWERCASE_LETTERS = set(string.ascii_lowercase)
UPPERCASE_LETTERS = set(string.ascii_uppercase)
NUMBERS = set(string.digits)
SYMBOLS = set(string.punctuation)


def password_validator(password):
    if len(password) < MIN_PASSWORD_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
        raise ValidationError(PASSWORD_LENGTH_VALIDATION_FAILED)

    _password = set(password)
    password_not_contains = _password.isdisjoint

    if password_not_contains(LOWERCASE_LETTERS) or password_not_contains(UPPERCASE_LETTERS) or\
            password_not_contains(NUMBERS) or password_not_contains(SYMBOLS):
        raise ValidationError(PASSWORD_CONSTRAINS_NOT_MET)

    return password
