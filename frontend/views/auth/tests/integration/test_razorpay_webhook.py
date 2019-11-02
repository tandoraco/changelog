import json

import pytest
from django.test import Client
from django.urls import reverse

from v1.accounts.models import AngelUser, Subscription

client = Client()
path = reverse('razorpay-webhook')


@pytest.mark.django_db
def test_angeluser(razorpay_webhook_data):
    # if the paid user is not in User table, create an angel user
    assert AngelUser.objects.count() == 0

    response = client.post(path=path, data=razorpay_webhook_data, content_type='application/json')
    assert response.status_code == 200

    assert AngelUser.objects.count() == 1

    angel = AngelUser.objects.get()
    assert json.loads(angel.data) == razorpay_webhook_data


@pytest.mark.django_db
def test_subscription_created(trial_user, razorpay_webhook_data):
    assert trial_user.company.is_trial_account
    trial_user.email = 'test@test.com'
    trial_user.save()

    # for a trial user, subscription entry is not present
    with pytest.raises(Subscription.DoesNotExist):
        Subscription.objects.get(company=trial_user.company)

    response = client.post(path=path, data=razorpay_webhook_data, content_type='application/json')

    assert response.status_code == 200

    trial_user.refresh_from_db()
    assert not trial_user.company.is_trial_account

    subscription = Subscription.objects.get(company=trial_user.company)
    assert json.loads(subscription.razorpay_data) == razorpay_webhook_data
