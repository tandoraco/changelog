import json

from django.utils import timezone

from v1.accounts.models import User, Subscription, AngelUser


def save_subscription_details(data):
    razorpay_id = data['account_id']
    email = data['payload']['payment']['entity']['email']
    try:
        user = User.objects.get(email=email)
        company = user.company
        subscription, created = Subscription.objects.get_or_create(razorpay_account_id=razorpay_id)

        if not subscription.company:
            subscription.company = company

        subscription.razorpay_data = json.dumps(data)
        subscription.last_paid_time = timezone.now()
        subscription.save()

        if company.is_trial_account:
            company.is_trial_account = False
            company.save()

    except User.DoesNotExist:
        AngelUser.objects.create(email=email, data=json.dumps(data))
