import pytest

from v1.accounts.utils import hash_password, verify_password


@pytest.mark.django_db
@pytest.mark.unit
def test_verify_password(admin, company_data):
    assert verify_password(admin, company_data['password'])

    new_password = 'Newpassword345.'
    admin.password_hash = hash_password(new_password)
    admin.save()
    assert verify_password(admin, new_password)
