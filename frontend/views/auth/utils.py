import json

from django.utils import timezone

from v1.accounts.models import User, Subscription, AngelUser, PendingInvoice


def save_subscription_details(data):
    razorpay_id = data['account_id']
    payment_payload_entity = data['payload']['payment']['entity']
    email = payment_payload_entity['email']
    event = data['event']
    try:
        if event == 'invoice.paid':
            invoice_id = payment_payload_entity['invoice_id']
            try:
                pending_invoice = PendingInvoice.objects.get(invoice_id=invoice_id)
                pending_invoice.delete()
            except PendingInvoice.DoesNotExist:
                raise User.DoesNotExist

        user = User.objects.get(email=email)
        company = user.company
        subscription, created = Subscription.objects.get_or_create(company=company)
        subscription.razorpay_account_id = razorpay_id
        subscription.razorpay_data = json.dumps(data)
        subscription.invoice_id = payment_payload_entity['invoice_id']
        subscription.last_paid_time = timezone.now()
        subscription.save()

        if company.is_trial_account:
            company.is_trial_account = False
            company.save()

    except User.DoesNotExist:
        AngelUser.objects.create(email=email, data=json.dumps(data))
