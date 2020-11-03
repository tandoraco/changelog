import json

from django.conf import settings

from v1.utils import send_to_slack


def post_new_affiliate_signup_to_slack(sender, instance, created, **kwargs):
    if created:
        send_to_slack(f'New affiliate signup -> {str(instance)}')


def notify_new_company_signup_in_slack(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:
        data = {
            'company_name': instance.company_name,
            'website': instance.website,
            'admin_email_id': instance.admin.email,
            'admin_name': instance.admin.name,
        }
        if 'test.com' not in data['admin_email_id']:
            data = json.dumps(data, indent=4)
            send_to_slack(f'New company signup notification\n ```{data}```')
