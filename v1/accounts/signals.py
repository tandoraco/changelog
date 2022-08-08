import json

import requests
from django.conf import settings
from django.utils.text import slugify

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


def create_custom_domain_in_user_custom_domain(sender, instance, created, **kwargs):
    headers = {
        'Authorization': f'Bearer {settings.USER_CUSTOM_DOMAIN_TOKEN}'
    }
    data = {
        'domain': instance.domain_name
    }
    if created and not settings.DEBUG:
        response = requests.post(url=settings.USER_CUSTOM_DOMAIN_URL, json=data, headers=headers)
        if not response.ok:
            raise RuntimeError('Unable to create a custom domain.. Please try again later.')
    else:
        print(data)


def save_bio_link(sender, instance, created, **kwargs):
    if created:
        instance.website = f"https://byol.ink/{slugify(instance.company_name)}"
        instance.save()

        data = {
            'user_name': slugify(instance.company_name),
            'company_name': slugify(instance.company_name)
        }
        url = "https://byol.ink/tc/biolink"
        headers = {
            'Authorization': f'Bearer {settings.TANDORA_CHANGELOG_KEY}'
        }

        if not settings.DEBUG:
            resp = requests.post(url, data=data, headers=headers)

            if resp:
                print('success')
            else:
                print(resp.content)
