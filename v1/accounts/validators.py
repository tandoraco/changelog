import string

from django import forms
from rest_framework import serializers

from v1.accounts.constants import (PASSWORD_CONSTRAINTS_NOT_MET,
                                   PASSWORD_LENGTH_VALIDATION_FAILED,
                                   MIN_PASSWORD_LENGTH,
                                   MAX_PASSWORD_LENGTH, SPECIAL_CHARACTERS_NOT_ALLOWED)

LOWERCASE_LETTERS = set(string.ascii_lowercase)
UPPERCASE_LETTERS = set(string.ascii_uppercase)
NUMBERS = set(string.digits)
SYMBOLS = set(string.punctuation)


def password_validator(password, form=False):
    validation_error = forms.ValidationError if form else serializers.ValidationError

    if len(password) < MIN_PASSWORD_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
        raise validation_error(PASSWORD_LENGTH_VALIDATION_FAILED)

    _password = set(password)
    password_not_contains = _password.isdisjoint

    if password_not_contains(LOWERCASE_LETTERS) or password_not_contains(UPPERCASE_LETTERS) or\
            password_not_contains(NUMBERS) or password_not_contains(SYMBOLS):
        raise validation_error(PASSWORD_CONSTRAINTS_NOT_MET)

    return password


def form_password_validator(password):
    return password_validator(password, form=True)


def no_symbols_validator(value, form=False):
    validation_error = forms.ValidationError if form else serializers.ValidationError

    _value = set(value)
    value_not_contains = _value.isdisjoint

    if value_not_contains(SYMBOLS):
        return value

    raise validation_error(SPECIAL_CHARACTERS_NOT_ALLOWED)


def form_no_symbols_validator(value):
    return no_symbols_validator(value, form=True)
