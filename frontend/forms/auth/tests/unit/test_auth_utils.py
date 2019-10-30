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
    session = {
        'company-id': company.id
    }
    mock_request = namedtuple('mock_request', 'session')
    request = mock_request(session=session)
    assert not is_trial_expired(request)

    company.is_trial_account = True
    company.save()
    company.refresh_from_db()
