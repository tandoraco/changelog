import pytest
from rest_framework.serializers import ValidationError

from v1.accounts.constants import (PASSWORD_CONSTRAINTS_NOT_MET,
                                   PASSWORD_LENGTH_VALIDATION_FAILED, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
from v1.accounts.validators import password_validator


@pytest.mark.unit
def test_password_validator():
    password = "a" * (MIN_PASSWORD_LENGTH - 1)

    with pytest.raises(ValidationError) as e:
        password_validator(password)
    assert e.value.args[0] == PASSWORD_LENGTH_VALIDATION_FAILED

    password = "a" * (MAX_PASSWORD_LENGTH + 1)

    with pytest.raises(ValidationError) as e:
        password_validator(password)
    assert e.value.args[0] == PASSWORD_LENGTH_VALIDATION_FAILED

    password = "a" * MIN_PASSWORD_LENGTH
    with pytest.raises(ValidationError) as e:
        password_validator(password)
    assert e.value.args[0] == PASSWORD_CONSTRAINTS_NOT_MET

    password = "testtest"
    with pytest.raises(ValidationError) as e:
        password_validator(password)
    assert e.value.args[0] == PASSWORD_CONSTRAINTS_NOT_MET

    password = "testtestT"
    with pytest.raises(ValidationError) as e:
        password_validator(password)
    assert e.value.args[0] == PASSWORD_CONSTRAINTS_NOT_MET

    password = "testtestT1"
    with pytest.raises(ValidationError) as e:
        password_validator(password)
    assert e.value.args[0] == PASSWORD_CONSTRAINTS_NOT_MET

    password = "testtestT1@"
    assert password_validator(password) == password
