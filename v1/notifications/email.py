from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail

from v1.notifications.email_templates.json_templates import TEMPLATES

FROM_ADDRESS = "no-reply@tandora.co"


class Email(object):

    @classmethod
    def send_mail(cls, template, model):
        if hasattr(model, "email"):
            recipient_email = getattr(model, "email")
        elif hasattr(model, "admin"):
            recipient_email = model.admin.email
        elif hasattr(model, "user"):
            recipient_email = model.user.email

        if recipient_email:
            send_mail(
                template['subject'],
                template['body'],
                FROM_ADDRESS,
                [recipient_email]
            )
        else:
            # Todo: log misses
            pass


def send_forgot_password_mail(sender, instance, created, **kwargs):
    from v1.accounts.models import ForgotPassword
    if created:
        template = TEMPLATES['forgot_password']
        reset_password_link = urljoin(settings.HOST, f'reset-password/{instance.token}')
        template['body'] = template['body'].format(link=reset_password_link)
        Email.send_mail(template, ForgotPassword)
