from v1.utils import send_to_slack


def post_new_affiliate_signup_to_slack(sender, instance, created, **kwargs):
    if created:
        send_to_slack(f'New affiliate signup -> {str(instance)}')
