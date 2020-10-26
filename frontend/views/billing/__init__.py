import datetime
import json
from json import JSONDecodeError

from django.apps import apps
from django.shortcuts import render

from frontend.custom.decorators import is_admin, is_authenticated
from v1.accounts.models import PendingInvoice

DAYS_IN_A_YEAR = 365


@is_authenticated
@is_admin
def billing_page(request):
    billing_keys = ['plan_name', 'expires_on', 'billing_name', 'billing_email', 'billing_address', 'invoice']

    try:
        subscription = request.user.company.subscription
        company = request.user.company
        expires_on = subscription.last_paid_time + datetime.timedelta(
            days=DAYS_IN_A_YEAR) if subscription.last_paid_time else '~'

        billing_address = '~'
        try:
            json.loads(subscription.razorpay_data)
        except JSONDecodeError:
            pass

        invoice_url = subscription.invoice_url
        if invoice_url == '~':
            invoice = '~'
        else:
            invoice = f'<a href="{invoice_url}">Click here</a> to download invoice'

        context = {
            'plan_name': subscription.plan.name,
            'expires_on': expires_on,
            'billing_name': company.admin.name,
            'billing_email': company.admin.email,
            'billing_address': billing_address,
            'invoice': invoice
        }

        try:
            pending_invoice = PendingInvoice.objects.get(company=company)
            pending_invoice_data = {
                'pending_invoice': True,
                'pending_invoice_url': pending_invoice.short_url,
                'pending_invoice_expiry_time': pending_invoice.expiry_time
            }
            context.update(**pending_invoice_data)
        except PendingInvoice.DoesNotExist:
            pass
    except apps.get_model('v1', 'Subscription').DoesNotExist:
        context = {key: '~' for key in billing_keys}

    return render(request, 'staff/billing.html', context=context)
