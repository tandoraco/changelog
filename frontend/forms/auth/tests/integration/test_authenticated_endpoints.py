from datetime import timedelta
from urllib.parse import urlparse, parse_qs

import mock
import pytest
from django.test import Client
from rest_framework import status

from frontend.constants import FREE_TRIAL_PERIOD_IN_DAYS

AUTHENTICATED_ENDPOINTS = [
    '/staff',
    '/staff/create-changelog',
    '/staff/manage/categories',
    '/staff/manage/categories/create-category',
    '/staff/manage/profile/company',
    '/staff/manage/profile/myself',
    '/staff/manage/widget',
]


@pytest.mark.django_db
@pytest.mark.integration
class TestAuthenticatedEndpoints:
    client = Client()

    def test_authenticated_endpoints_without_logging_in(self, user, company):
        # When we do not login and hit an endpoint that requires authentication
        # we will be redirected to login page with redirect_to set to requested endpoint

        for endpoint in AUTHENTICATED_ENDPOINTS:
            response = self.client.get(endpoint)
            assert response.status_code == status.HTTP_302_FOUND
            assert 'redirect_to' in response.url

            parsed_response_url = urlparse(response.url)
            parsed_response_url_query = parse_qs(parsed_response_url.query)
            assert parsed_response_url_query['redirect_to'][0] == endpoint

    def test_trial_check(self, company, user):
        company.is_trial_account = True
        company.save()
        company.refresh_from_db()

        with mock.patch('django.utils.timezone.now') as timezone_now:
            timezone_now.return_value = company.created_time + timedelta(days=FREE_TRIAL_PERIOD_IN_DAYS + 1)

            for endpoint in AUTHENTICATED_ENDPOINTS:
                response = self.client.get(endpoint)
                assert response.status_code == status.HTTP_302_FOUND
                assert 'redirect_to' in response.url
                assert 'login' in response.url
