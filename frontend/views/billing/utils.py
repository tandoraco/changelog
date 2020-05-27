import datetime

from django.conf import settings
import razorpay


def generate_inr_invoice(plan, company, yearly=True):
    if not plan:
        raise ValueError('Plan is required.')

    if yearly:
        amount = int(plan.yearly_price)
        period = 'year'
    else:
        amount = int(plan.monthly_price)
        period = 'month'

    invoice_expiry_time = int((datetime.datetime.now() + datetime.timedelta(weeks=1)).timestamp())

    data = {
        'type': 'invoice',
        'description': f'Invoice for purchase of 1 {period} subscription of Tandora Changelog',
        'partial_payment': False,
        'customer': {
            'name': company.admin.name,
            'email': company.admin.email,
        },
        'line_items': [
            {
                'name': f'Tandora Changelog - {plan.name} plan',
                'description': f'{period.title()}ly subscription for Tandora Changelog',
                'amount': amount,
                'currency': 'INR',
                'quantity': 1
            }
        ],
        'sms_notify': 0,
        'email_notify': 1,
        'expire_by': invoice_expiry_time
    }

    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))
    invoice = razorpay_client.invoice.create(data=data)
    return invoice
