import json

from v1.utils import send_to_slack


def post_new_affiliate_signup_to_slack(sender, instance, created, **kwargs):
    if created:
        send_to_slack(f'New affiliate signup -> {str(instance)}')


def notify_new_company_signup_in_slack(sender, instance, created, **kwargs):
    if created:
        data = {
            'company_name': instance.company_name,
            'website': instance.website,
            'admin_email_id': instance.admin.email,
            'admin_name': instance.admin.name,
        }
        data = json.dumps(data, indent=4)
        send_to_slack(f'New company signup notification\n ```{data}```')
