from collections import namedtuple
from datetime import timedelta

import mock
import pytest

from frontend.constants import FREE_TRIAL_PERIOD_IN_DAYS
from frontend.forms.auth.utils import is_trial_expired


@pytest.mark.django_db
@pytest.mark.unit
def test_is_trial_expired(company):
    # by default trial is false for all accounts
    # this is so to enable smooth migration for existing setups
    assert not company.is_trial_account

    session = {
        'company-id': company.id
    }
    mock_request = namedtuple('mock_request', 'session')
    request = mock_request(session=session)
    assert not is_trial_expired(request)

    company.is_trial_account = True
    company.save()
    company.refresh_from_db()

    # if is_trial_account is true, account is valid only for seven days
    # so is_trial_expired will be false within trial period
    for i in range(FREE_TRIAL_PERIOD_IN_DAYS-1):
        with mock.patch('django.utils.timezone.now') as timezone_now:
            timezone_now.return_value = company.created_time + timedelta(days=i)
            assert not is_trial_expired(request)

    # after trial period, is_trial_expired will be true
    with mock.patch('django.utils.timezone.now') as timezone_now:
        timezone_now.return_value = company.created_time + timedelta(FREE_TRIAL_PERIOD_IN_DAYS + 1)
        assert is_trial_expired(request)
