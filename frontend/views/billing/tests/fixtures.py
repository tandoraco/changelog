import json

import pytest


@pytest.fixture
def razorpay_webhook_invoice_data():
    return json.loads('''
    {
  "entity": "event",
  "account_id": "acc_DS11bHy6VsKIm1",
  "event": "invoice.paid",
  "contains": [
    "payment",
    "order",
    "invoice"
  ],
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_EvDHLLHjDrRSYu",
        "entity": "payment",
        "amount": 60000,
        "currency": "INR",
        "status": "captured",
        "order_id": "order_EvDD7cYZTRixBP",
        "invoice_id": "inv_EvDD7ZfIVsHYgR",
        "international": false,
        "method": "upi",
        "amount_refunded": 0,
        "refund_status": null,
        "captured": true,
        "description": "Invoice #inv_EvDD7ZfIVsHYgR",
        "card_id": null,
        "bank": null,
        "wallet": null,
        "vpa": "test@okicici",
        "email": "test@localhost.com",
        "contact": "+911234567890",
        "notes": [],
        "fee": 1416,
        "tax": 216,
        "error_code": null,
        "error_description": null,
        "error_source": null,
        "error_step": null,
        "error_reason": null,
        "created_at": 1590545763
      }
    },
    "order": {
      "entity": {
        "id": "order_EvDD7cYZTRixBP",
        "entity": "order",
        "amount": 60000,
        "amount_paid": 60000,
        "amount_due": 0,
        "currency": "INR",
        "receipt": null,
        "offer_id": null,
        "offers": {
          "entity": "collection",
          "count": 0,
          "items": []
        },
        "status": "paid",
        "attempts": 1,
        "notes": [],
        "created_at": 1590545524
      }
    },
    "invoice": {
      "entity": {
        "id": "inv_EvDD7ZfIVsHYgR",
        "entity": "invoice",
        "receipt": null,
        "invoice_number": null,
        "customer_id": "cust_EvDD7Zx5bryyeg",
        "customer_details": {
          "id": "cust_EvDD7Zx5bryyeg",
          "name": "Test",
          "email": "test@localhost.com",
          "contact": null,
          "gstin": null,
          "billing_address": null,
          "shipping_address": null,
          "customer_name": "Test",
          "customer_email": "test@localhost.com",
          "customer_contact": null
        },
        "order_id": "order_EvDD7cYZTRixBP",
        "payment_id": "pay_EvDHLLHjDrRSYu",
        "status": "paid",
        "expire_by": 1591150323,
        "issued_at": 1590545524,
        "paid_at": 1590545764,
        "cancelled_at": null,
        "expired_at": null,
        "sms_status": null,
        "email_status": "sent",
        "date": 1590545523,
        "terms": null,
        "partial_payment": false,
        "gross_amount": 60000,
        "tax_amount": 0,
        "taxable_amount": 60000,
        "amount": 60000,
        "amount_paid": 60000,
        "amount_due": 0,
        "first_payment_min_amount": null,
        "currency": "INR",
        "currency_symbol": "₹",
        "description": "Invoice for purchase of 1 year subscription of Tandora Changelog",
        "notes": [],
        "comment": null,
        "short_url": "https://rzp.io/i/N422gyq",
        "view_less": true,
        "billing_start": null,
        "billing_end": null,
        "type": "invoice",
        "group_taxes_discounts": false,
        "supply_state_code": null,
        "user_id": null,
        "created_at": 1590545524,
        "idempotency_key": null
      }
    }
  },
  "created_at": 1590545764
}
    ''')
