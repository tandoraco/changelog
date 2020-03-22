from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from v1.notifications.email_templates.json_templates import TEMPLATES

FROM_ADDRESS = "no-reply@tandora.co"


class Email(object):

    @classmethod
    def send_mail(cls, template, model, sender_email=None):
        recipient_email = ""
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
                FROM_ADDRESS if not sender_email else sender_email,
                [recipient_email]
            )
        else:
            # Todo: log misses
            pass


def send_verification_mail(template_name, link, instance):
    template = TEMPLATES[template_name]
    template['body'] = template['body'].format(link=link)
    Email.send_mail(template, instance)


def send_forgot_password_mail(sender, instance, created, **kwargs):
    if created:
        reset_password_link = urljoin(settings.HOST, f'reset-password/{instance.token}')
        send_verification_mail('forgot_password', reset_password_link, instance)


@transaction.atomic
def send_user_verification_email(sender, instance, created, **kwargs):
    if created:
        from v1.accounts.models import PendingUser
        pending_user = PendingUser.objects.create(user=instance)
        user_verification_link = urljoin(settings.HOST, f'verify-user/{pending_user.uuid}')
        send_verification_mail('user_verification', user_verification_link, pending_user)
